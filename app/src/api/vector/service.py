import logging

from fastapi import UploadFile
from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.src.api.vector.constants import QUERY_TEMPLATE
from app.src.api.vector.documents.service import DocumentsService
from app.src.api.vector.schemas import ChatResponse, VectorDbInfo
from app.src.api.vector.utils import extract_necessary_message_data
from app.src.core.config import settings
from app.src.core.ml_models import GigaChatClient

logger = logging.getLogger(__name__)


class VectorRagStorageService:
    def __init__(
        self,
        documents_service: DocumentsService,
        vector_store: Chroma,
        max_documents: int,
    ) -> None:
        self._documents_service = documents_service
        self._vs_repository = vector_store
        # В ChromaDB за раз можно вставить только 5461 эмбеддингов (документов).
        # Если количество документов больше маскимального, то они делятся и по отдельности вставляются в БД
        self._max_documents = max_documents

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
        """
        Возвращает все уникальные значения метатега 'source' (названия файлов, которые уже были загружены).\n
        В будущем нужно добавить БД SQLite и записывать, а далее и забирать, названия файлов при эмбеддинге туда.
        При большом количестве эмбеддингов в хранилище текущий вариант будет неэффективен.
        """

        total_docs = self._vs_repository._collection.count()
        step = 20000
        metadata = []

        for i in range(0, total_docs, step):
            metadata.extend(
                self._vs_repository.get(
                    include=["metadatas"],
                    offset=i,
                    limit=step,
                )["metadatas"]
            )

        return list(set([meta["source"] for meta in metadata if meta]))

    def get_downloaded_files(self) -> list[str]:
        """Возвращает загруженные в БД файлы"""

        logger.info("Start getting downloaded files")
        downloaded_files = self._get_all_docs_sources()
        logger.info("Downloaded files are got")

        return downloaded_files

    def _get_insert_batches(self, chunks: list[Document]) -> list[list[Document]]:
        """Делит данные для вставки в векторную БД на батчи (если количество превышает self._max_documents)"""

        logger.debug("Spliting documents into batches")
        batches = []

        if len(chunks) > self._max_documents:
            batches = []

            for i in range(0, len(chunks), self._max_documents):
                batches.append(chunks[i : i + self._max_documents])
        else:
            batches.append(chunks)

        logger.info(f"{len(batches)} batches will be inserted in ChromaDB")
        return batches

    def add_documents(self, files: list[UploadFile]) -> list[str]:
        """Добавляет разделенные на чанки документы в векторную БД. Возвращает ID записей в векторной БД"""

        logger.info("Start adding documents in vector store")
        exclude_sources = self._get_all_docs_sources()
        logger.debug(f"Exclude sources: {', '.join(exclude_sources)}")
        docs_chunks = self._documents_service.get_documents_splitted_by_chunks(
            files, exclude_sources
        )

        if not docs_chunks:
            logger.info("There are no new documents")
            return []

        ids = []
        for batch in self._get_insert_batches(docs_chunks):
            ids.extend(self._vs_repository.add_documents(batch))
            logger.debug("Batch is inserted")

        logger.info("Documents are added")
        return ids

    def get_documents(self, query: str, docs_count: int) -> list[tuple[str, float]]:
        """Возвращает документы, наиболее релевантные к запросу"""

        docs = self._vs_repository.similarity_search_with_score(
            query=query, k=docs_count
        )

        return [(doc.page_content, score) for doc, score in docs]


class VectorRagChatService:
    def __init__(self, vector_store: Chroma, llm: GigaChatClient):
        self._vs_repository = vector_store
        self._llm = llm

    def chat(self, query: str, temperature: float, docs_count: int) -> ChatResponse:
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

        if temperature != 0.0:
            message = self._llm.get_model_with_new_settings(
                temperature=temperature
            ).invoke(augmented_query)
        else:
            message = self._llm.invoke(augmented_query)

        logger.info("Answer is got")
        return ChatResponse(
            query=query,
            relevant_info=relevant_docs_content,
            **extract_necessary_message_data(message),
        )
