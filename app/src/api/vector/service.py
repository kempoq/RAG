import logging

from langchain_chroma import Chroma
from langchain_gigachat.chat_models import GigaChat

from app.src.api.vector.constants import QUERY_TEMPLATE
from app.src.api.vector.documents.service import DocumentsService

logger = logging.getLogger(__name__)


class VectorRagService:
    def __init__(
        self, documents_service: DocumentsService, vector_store: Chroma, llm: GigaChat
    ) -> None:
        self._documents_service = documents_service
        self._vs_repository = vector_store
        self._llm = llm

    def _get_all_docs_sources(self) -> list[str]:
        """Возвращает все уникальные значения метатега 'source' (названия файлов, которые уже были загружены)"""

        metadata = self._vs_repository.get(include=["metadatas"])["metadatas"]
        return list(set([meta["source"] for meta in metadata if meta]))

    def get_filenames(self, ext: str = "txt") -> tuple[list[str], list[str]]:
        """Возвращает загруженные и еще не загруженные в БД файлы"""

        downloaded_files = self._get_all_docs_sources()
        all_files = self._documents_service.get_filenames(ext)

        return downloaded_files, list(set(all_files) - set(downloaded_files))

    def add_documents(self, ext: str = "txt") -> tuple[list[str], list[str]]:
        """Добавляет разделенные на чанки документы в векторную БД"""

        logger.info("Start adding documents in vector store")
        exclude_sources = self._get_all_docs_sources()
        files, docs_chunks = self._documents_service.get_documents_by_chunks(
            exclude_sources, ext
        )

        if not docs_chunks:
            logger.info("There are no new documents")
            return [], []

        ids = self._vs_repository.add_documents(docs_chunks)

        logger.info("Documents are inserted")
        return files, ids

    def chat(self, query: str, docs_count: int = 3) -> str:
        """
        Реализует логику RAG: отправляет запрос, дополненный данными из векторной БД, в LLM.
        Далее возвращает ответ
        """

        logger.info("Start chatting using simple RAG")
        relevant_docs = self._vs_repository.similarity_search(query, k=docs_count)
        augmented_query = QUERY_TEMPLATE.format(
            user_query=query,
            relevant_information="\n".join(
                [rdoc.page_content for rdoc in relevant_docs]
            ),
        )

        answer = self._llm.invoke(augmented_query).content

        logger.info("Answer is got")
        return answer
