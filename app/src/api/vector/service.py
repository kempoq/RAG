from langchain_chroma import Chroma

from app.src.api.vector.documents.service import DocumentsService


class VectorRagService:
    def __init__(
        self, documents_service: DocumentsService, vector_store: Chroma
    ) -> None:
        self._documents_service = documents_service
        self._vs_repository = vector_store

    def add_documents(self, ext: str = "txt") -> tuple[list[str], list[str]]:
        """Добавляет разделенные на чанки документы в векторную БД"""

        print("Start adding documents in vector store")
        files, docs_chunks = self._documents_service.get_documents_by_chunks(ext)

        if not docs_chunks:
            print("There are no new documents")
            return []

        ids = self._vs_repository.add_documents(docs_chunks)

        print("Documents are inserted")
        return files, ids
