"""
main.py
Векторный RAG: ChromaDB + эмбеддинги с HuggingFace (deepvk/USER-bge-m3).
"""

import os
from pathlib import Path

import chromadb
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ---------------------------------------------------------------------------
# Конфигурация
# ---------------------------------------------------------------------------

EMBEDDING_MODEL = "deepvk/USER-bge-m3"
COLLECTION_NAME = "rag"
VDB_DIR = str(Path(__file__).parent / ".chroma")
FILES_DIR = Path(__file__).parent / "assets"


# ---------------------------------------------------------------------------
# Вспомогательные функции
# ---------------------------------------------------------------------------

def get_embedding_model(model_name: str = EMBEDDING_MODEL) -> HuggingFaceEmbeddings:
    """
    Загружает модель с HuggingFace (кешируется локально после первой загрузки).
    deepvk/USER-bge-m3 — лучшая публичная модель для русских технических текстов.
    """
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": "cpu"},        # поменяй на "cuda" если есть GPU
        encode_kwargs={"normalize_embeddings": True},
    )


def get_vectorstore(embedding_model: HuggingFaceEmbeddings) -> Chroma:
    """Возвращает персистентное хранилище ChromaDB."""
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_model,
        persist_directory=VDB_DIR,
    )


def load_documents(files_dir: Path = FILES_DIR) -> list[Document]:
    """Читает все .txt файлы из папки assets/."""
    docs = []
    for path in files_dir.glob("*.txt"):
        with open(path, encoding="utf-8") as f:
            docs.append(Document(page_content=f.read(), metadata={"source": path.name}))
    return docs


def get_text_splitter(
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True,
    )


def index_documents(vectorstore: Chroma, files_dir: Path = FILES_DIR) -> int:
    """Загружает и индексирует документы из assets/. Возвращает кол-во чанков."""
    docs = load_documents(files_dir)
    if not docs:
        print(f"⚠️  Нет .txt файлов в {files_dir}")
        return 0

    splitter = get_text_splitter()
    chunks = splitter.split_documents(docs)
    vectorstore.add_documents(chunks)
    print(f"✅ Проиндексировано файлов: {len(docs)}, чанков: {len(chunks)}")
    return len(chunks)


# ---------------------------------------------------------------------------
# Основной запуск
# ---------------------------------------------------------------------------

def main() -> None:
    print(f"⏳ Загрузка модели {EMBEDDING_MODEL} с HuggingFace...")
    em = get_embedding_model()
    print("✅ Модель загружена.")

    vs = get_vectorstore(em)

    # Если коллекция пустая — индексируем документы
    if vs._collection.count() == 0:
        index_documents(vs)

    # Тестовый запрос
    query = "кислотное выщелачивание урана"
    print(f"\n🔍 Запрос: {query}")
    results = vs.similarity_search(query, k=3)

    for i, doc in enumerate(results, 1):
        source = doc.metadata.get("source", "—")
        print(f"\n[{i}] {source}")
        print(doc.page_content[:300], "...")


if __name__ == "__main__":
    main()
