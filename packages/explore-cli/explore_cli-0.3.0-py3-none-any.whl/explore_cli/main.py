import os
import logging

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "ERROR").upper())

import argparse
import chromadb
import hashlib
import gnureadline as readline
import textwrap
import toml

from chromadb.config import Settings
from chromadb.utils import embedding_functions
from dataclasses import dataclass
from fnmatch import fnmatch
from keybert.llm import OpenAI as KeyBERTOpenAI
from keybert import KeyLLM
from openai import OpenAI
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern
from tqdm import tqdm

IGNORED_PATTERNS = [
    "**/.git/*",
    "*.tmp",
    "*.log",
    "*.swp",
    "*.bak",
    "**/node_modules/*",
    "*.sock",
]
# disable huggingface tokenizers parallelism, it was giving a warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

logger = logging.getLogger()


@dataclass
class Config:
    openai_api_key: str
    openai_base_url: str
    openai_model: str
    db_path: str
    history_file: str
    num_docs: int
    num_context_docs: int
    doc_max_length: int

    @classmethod
    def load(cls, config_path):
        with open(config_path, "a+") as f:
            # Create the file if it doesn't exist
            pass
        with open(config_path, "r") as f:
            config = toml.load(f)
        get = lambda key, default: os.getenv(key.upper(), config.get(key, default))
        get_required = lambda key: os.getenv(key.upper(), config[key])
        return cls(
            openai_api_key=get_required("openai_api_key"),
            openai_base_url=get("openai_base_url", "https://api.openai.com/v1"),
            openai_model=get("openai_model", "gpt-4o-mini"),
            db_path=os.path.join(os.getenv("HOME"), ".explore", "db"),
            history_file=os.path.join(os.getenv("HOME"), ".explore", "history"),
            num_docs=int(get("num_docs", 5)),
            num_context_docs=int(get("num_context_docs", 2)),
            doc_max_length=int(get("doc_max_length", 10000)),
        )


def collection_name(directory):
    return directory.replace("/", "_").strip("_")


def extract_keywords(kw_extractor, text):
    keywords = set(kw_extractor.extract_keywords(text)[0])
    keywords = keywords.union({k.lower() for k in keywords})
    return [k.strip("'\" ") for k in keywords]


def load_gitignore(directory):
    gitignore_path = os.path.join(directory, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as f:
            return PathSpec.from_lines(GitWildMatchPattern, f)
    return None


def index_directory(
    client,
    embedding_function,
    directory,
    ignore_gitignore=True,
    disable_progress_bar=False,
    reindex=False,
):
    name = collection_name(directory)
    if reindex:
        try:
            client.delete_collection(name=name)
        except ValueError:
            pass
    collection = client.get_or_create_collection(
        name=name, embedding_function=embedding_function
    )

    pathspec = load_gitignore(directory) if ignore_gitignore else None

    count_progress = tqdm(
        desc="Collecting files", unit=" files", disable=disable_progress_bar
    )
    files = []
    for root, _, dir_files in os.walk(directory):
        for file in dir_files:
            if not (
                any(
                    fnmatch(os.path.join(root, file), pattern)
                    for pattern in IGNORED_PATTERNS
                )
                or (pathspec and pathspec.match_file(file))
            ):
                files.append(os.path.join(root, file))
                count_progress.update(1)

    count_progress.close()

    progress_bar = tqdm(
        total=len(files),
        desc="Indexing files",
        unit=" files",
        miniters=1,
        disable=disable_progress_bar,
    )

    for file_path in files:
        doc_id = hashlib.md5(file_path.encode("utf-8")).hexdigest()
        modified_time = os.path.getmtime(file_path)
        get_res = collection.get(ids=[doc_id], include=["metadatas"], limit=1)
        if (
            len(get_res["ids"]) > 0
            and get_res["metadatas"][0].get("modified_time", -1.0) == modified_time
            and not reindex
        ):
            progress_bar.update(1)
            continue
        with open(file_path, "r") as f:
            try:
                content = f"{file_path}:\n\n{f.read()}"
                collection.upsert(
                    documents=[content],
                    ids=[doc_id],
                    metadatas=[{"path": file_path, "modified_time": modified_time}],
                )
                progress_bar.update(1)
            except UnicodeDecodeError:
                logger.warning(f"Invalid UTF-8: {file_path}. Skipping")
                progress_bar.update(1)
    progress_bar.close()
    return collection


def retrieve_documents(kw_extractor, config, messages, collection, question):
    docs = {}

    initial_results = collection.query(
        query_texts=[question],
    )
    for doc, meta, distance in zip(
        initial_results["documents"][0],
        initial_results["metadatas"][0],
        initial_results["distances"][0],
    ):
        docs[meta["path"]] = {"document": doc, "distance": distance}

    logger.debug(
        f"Query documents: {[meta['path'] for meta in initial_results['metadatas'][0]]}"
    )

    search_keywords = extract_keywords(kw_extractor, question)
    logger.debug(f"Keywords: {search_keywords}")
    if search_keywords and len(search_keywords) > 0:
        if len(search_keywords) > 1:
            where_document = {
                "$or": [{"$contains": keyword} for keyword in search_keywords]
            }
        else:
            where_document = {"$contains": search_keywords[0]}
        keyword_results = collection.query(
            query_texts=[question],
            where_document=where_document,
        )
        for doc, meta, distance in zip(
            keyword_results["documents"][0],
            keyword_results["metadatas"][0],
            keyword_results["distances"][0],
        ):
            if meta["path"] not in docs:
                docs[meta["path"]] = {"document": doc, "distance": distance}
        logger.debug(
            f"Keyword documents: {[meta['path'] for meta in keyword_results['metadatas'][0]]}"
        )

    # Sort by distance, take the top N then reverse so that more relevant documents are later in the prompt
    question_docs = list(
        reversed(
            [d["document"] for d in sorted(docs.values(), key=lambda d: d["distance"])][
                : config.num_docs
            ]
        )
    )

    if len(messages) > 1:
        conversation_history = " ".join(msg["content"] for msg in messages)
        additional_results = collection.query(
            query_texts=[conversation_history],
            n_results=config.num_context_docs,
        )
        context_docs = []
        for doc, meta in zip(
            additional_results["documents"][0], additional_results["metadatas"][0]
        ):
            if meta["path"] not in docs:
                context_docs.append(doc)

        logger.debug(
            f"Context documents: {[meta['path'] for meta in additional_results['metadatas'][0]]}"
        )
    else:
        context_docs = []

    return context_docs + question_docs


def query_codebase(openai_client, config, messages, question, documents):
    context_documents = "\n\n".join(
        [textwrap.shorten(doc, width=config.doc_max_length) for doc in documents]
    )

    messages.append(
        {
            "role": "user",
            "content": f"Answer the following question about the provided source documents, ignoring any documents that don't seem relevant: {question}",
        }
    )
    response_text = ""
    response = openai_client.chat.completions.create(
        model=config.openai_model,
        messages=[
            {
                "role": "system",
                "content": f"You are an expert in understanding and explaining code. You will be asked a question about a codebase, respond concisely.",
            },
            {"role": "user", "content": f"Relevant source files: {context_documents}"},
        ]
        + messages,
        stream=True,
    )

    for chunk in response:
        if len(chunk.choices) > 0:
            text = chunk.choices[0].delta.content or ""
            response_text += text
            yield text
    messages.append({"role": "assistant", "content": response_text})


def main():
    parser = argparse.ArgumentParser(
        description="Interactively explore a codebase with an LLM."
    )
    parser.add_argument("directory", help="The directory to index and explore.")
    parser.add_argument(
        "--skip-index",
        action="store_true",
        help="skip indexing the directory (warning: if the directory hasn't been indexed at least once, it will be indexed anyway)",
    )
    parser.add_argument(
        "--reindex", action="store_true", help="Reindex the whole directory"
    )
    parser.add_argument(
        "--no-ignore", action="store_true", help="Disable respecting .gitignore files"
    )
    parser.add_argument(
        "--documents-only",
        action="store_true",
        help="Only print documents, then exit. --question must be provided",
    )
    parser.add_argument(
        "--question", help="Initial question to ask (will prompt if not provided)"
    )
    parser.add_argument(
        "--no-progress-bar", help="Disable progress bar", action="store_true"
    )
    parser.add_argument(
        "--index-only", help="Only index the directory", action="store_true"
    )
    parser.add_argument(
        "--config",
        help="Path to the config file",
        default=os.path.join(os.getenv("HOME"), ".explore", "config.toml"),
    )
    args = parser.parse_args()

    directory = os.path.abspath(os.path.expanduser(args.directory))
    ignore_gitignore = not args.no_ignore
    documents_only = args.documents_only
    initial_question = args.question
    no_progress_bar = args.no_progress_bar
    index_only = args.index_only
    reindex = args.reindex
    config_path = args.config

    if documents_only and not initial_question:
        parser.error("--question is required when using --documents-only")

    messages = []
    config = Config.load(config_path)
    logger.debug(f"Config: {config}")
    os.makedirs(config.db_path, exist_ok=True)
    openai_client = OpenAI(
        api_key=config.openai_api_key, base_url=config.openai_base_url
    )
    kw_extractor = KeyLLM(
        KeyBERTOpenAI(model=config.openai_model, client=openai_client, chat=True)
    )
    client = chromadb.PersistentClient(
        path=config.db_path, settings=Settings(anonymized_telemetry=False)
    )
    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-mpnet-base-v2"
    )

    try:
        if args.skip_index:
            name = collection_name(directory)
            try:
                collection = client.get_collection(name=name)
            except ValueError:
                print(
                    f"Warning: No existing collection for {directory}. Indexing is required."
                )
                collection = index_directory(
                    client,
                    embedding_function,
                    directory,
                    ignore_gitignore,
                    disable_progress_bar=no_progress_bar,
                )
        else:
            collection = index_directory(
                client,
                embedding_function,
                directory,
                ignore_gitignore,
                disable_progress_bar=no_progress_bar,
                reindex=reindex,
            )

        if index_only:
            return

        if not os.path.exists(config.history_file):
            os.makedirs(os.path.dirname(config.history_file), exist_ok=True)
            with open(config.history_file, "wb"):
                pass  # create the file
        readline.read_history_file(config.history_file)
        looped = False
        while True:
            if initial_question and not looped:
                question = initial_question
            else:
                question = input(
                    "Ask a question about the codebase (or type 'exit' to quit): "
                )
            looped = True
            if question.lower() == "exit":
                break

            print("", flush=True)
            documents = retrieve_documents(
                kw_extractor, config, messages, collection, question
            )
            if documents_only:
                for doc in documents:
                    print(doc)
                break
            for part in query_codebase(
                openai_client, config, messages, question, documents
            ):
                print(part, end="", flush=True)
            print()  # For a new line after the full response
            readline.write_history_file(config.history_file)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

# TODO:
# - integrate with Emacs
