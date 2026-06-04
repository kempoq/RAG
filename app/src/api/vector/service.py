from langchain_chroma import Chroma

from app.src.api.vector.constants import QUERY_TEMPLATE
from app.src.api.vector.documents.service import DocumentsService


class DummyLLM:
    """Временная затычка, пока нет реальной LLM"""

    def chat(self, query: str) -> str:
        return query


class VectorRagService:
    def __init__(
        self, documents_service: DocumentsService, vector_store: Chroma
    ) -> None:
        self._documents_service = documents_service
        self._vs_repository = vector_store
        self._llm = DummyLLM()

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

    def chat(self, query: str, docs_count: int = 3) -> str:
        """
        Реализует логику RAG: отправляет запрос, дополненный данными из векторной БД, в LLM.
        Далее возвращает ответ
        """

        relevant_docs = self._vs_repository.similarity_search(query, k=docs_count)
        augmented_query = QUERY_TEMPLATE.format(
            user_query=query,
            relevant_information="\n".join(
                [rdoc.page_content for rdoc in relevant_docs]
            ),
        )

        answer = self._llm.chat(augmented_query)

        return answer
