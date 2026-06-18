import logging

from langchain_openai import ChatOpenAI

from app.src.api.no_rag.schemas import ChatResponse
from app.src.api.no_rag.utils import extract_necessary_message_data
from app.src.core.ml_models import GigaChatClient

logger = logging.getLogger(__name__)


class NoRagService:
    def __init__(self, llm: ChatOpenAI | GigaChatClient) -> None:
        self._llm = llm

    def chat(self, query: str) -> ChatResponse:
        """Возвращает ответ на вопрос от LLM"""

        logging.info("Start getting answer from LLM")
        message = self._llm.invoke(query)
        logging.info("Answer is got")

        return ChatResponse(query=query, **extract_necessary_message_data(message))
