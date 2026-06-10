import logging

from fastapi import UploadFile
from langchain_chroma import Chroma
from langchain_gigachat.chat_models import GigaChat

from app.src.api.vector.constants import QUERY_TEMPLATE
from app.src.api.vector.documents.service import DocumentsService
from app.src.api.vector.schemas import VectorDbInfo
from app.src.core.config import settings

logger = logging.getLogger(__name__)


class VectorRagService:
    def __init__(
        self, documents_service: DocumentsService, vector_store: Chroma
    ) -> None:
        self._documents_service = documents_service
        self._vs_repository = vector_store

    def get_info(self) -> VectorDbInfo:
        """Возвращает различные метаданные по векторной БД"""

        logger.info("Start getting vector storage info")
        total_docs = self._vs_repository._collection.count()

        vector_db_info = VectorDbInfo(
            total_docs=total_docs,
            embedding_model=settings.embedding_model_name,
        )

        logger.info("Vector storage info is got")
        return vector_db_info

    def _get_all_docs_sources(self) -> list[str]:
        """Возвращает все уникальные значения метатега 'source' (названия файлов, которые уже были загружены)"""

        metadata = self._vs_repository.get(include=["metadatas"])["metadatas"]
        return list(set([meta["source"] for meta in metadata if meta]))

    def get_downloaded_files(self) -> list[str]:
        """Возвращает загруженные в БД файлы"""

        logger.info("Start getting downloaded files")
        downloaded_files = self._get_all_docs_sources()
        logger.info("Downloaded files are got")

        return downloaded_files

    def add_documents(self, files: list[UploadFile]) -> list[str]:
        """Добавляет разделенные на чанки документы в векторную БД. Возвращает ID записей в векторной БД"""

        logger.info("Start adding documents in vector store")
        exclude_sources = self._get_all_docs_sources()
        logger.debug(f"Exclude sources: {', '.join(exclude_sources)}")
        docs_chunks = self._documents_service.get_document_chunks(
            files, exclude_sources
        )

        if not docs_chunks:
            logger.info("There are no new documents")
            return []

        ids = self._vs_repository.add_documents(docs_chunks)

        logger.info("Documents are added")
        return ids


class VectorRagChatService:
    def __init__(self, vector_store: Chroma, llm: GigaChat):
        self._vs_repository = vector_store
        self._llm = llm

    def chat(self, query: str, docs_count: int = 3) -> tuple[str, list[str]]:
        """
        Реализует логику RAG: отправляет запрос, дополненный данными из векторной БД, в LLM.
        Далее возвращает ответ
        """

        logger.info("Start chatting using simple RAG")
        relevant_docs = self._vs_repository.similarity_search(query, k=docs_count)
        relevant_docs_content = [rdoc.page_content for rdoc in relevant_docs]

        augmented_query = QUERY_TEMPLATE.format(
            user_query=query,
            relevant_information="\n".join(relevant_docs_content),
        )

        answer = self._llm.invoke(augmented_query).content

        logger.info("Answer is got")
        return answer, relevant_docs_content
