import logging

from app.src.api.no_rag.schemas import ChatResponse
from app.src.api.no_rag.utils import extract_necessary_message_data
from app.src.core.ml_models import GigaChatClient

logger = logging.getLogger(__name__)


class NoRagService:
    def __init__(self, llm: GigaChatClient) -> None:
        self._llm = llm

    def chat(self, query: str, temperature: float) -> ChatResponse:
        """Возвращает ответ на вопрос от LLM"""

        logging.info("Start getting answer from LLM")
        if temperature != 0:
            message = self._llm.get_model_with_new_settings(
                temperature=temperature
            ).invoke(query)
        else:
            message = self._llm.invoke(query)
        logging.info("Answer is got")

        return ChatResponse(query=query, **extract_necessary_message_data(message))
