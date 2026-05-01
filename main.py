import chromadb
from chromadb.api import ClientAPI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma


EMBEDDING_MODEL = "text-embedding-nomic-embed-text-v1.5"
COLLECTION_NAME = "rag"
VDB_DIR = "./.chroma"
FILES_DIR = "assets"


def get_db() -> ClientAPI:
    db = chromadb.PersistentClient(path="chromadb")
    return db


def get_document(path: str) -> Document:
    with open(path, encoding="utf-8") as f:
        return Document(page_content=f.read())


def get_text_splitter(
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    add_start_index: bool = True,
) -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=add_start_index,
    )


def get_embedding_model(
    model_name: str, base_url: str = "http://127.0.0.1:1234/v1"
) -> OpenAIEmbeddings:
    return OpenAIEmbeddings(
        model=model_name,
        base_url=base_url,
        check_embedding_ctx_length=False,
        openai_api_key="lm-studio",
    )


def main():
    em = get_embedding_model(model_name=EMBEDDING_MODEL)
    vs = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=em,
        persist_directory=VDB_DIR,
    )
    print(
        vs.similarity_search(
            query="Tell me something about fluorescent lamps",
            k=2,
        )
    )


if __name__ == "__main__":
    main()
