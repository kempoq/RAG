import logging

from langchain_openai import ChatOpenAI

from app.src.core.ml_models import GigaChatClient

logger = logging.getLogger(__name__)


class NoRagService:
    def __init__(self, llm: ChatOpenAI | GigaChatClient) -> None:
        self._llm = llm

    def chat(self, query: str) -> str:
        """Возвращает ответ на вопрос от LLM"""

        logging.info("Start getting answer from LLM")
        answer = self._llm.invoke(query)
        logging.info("Answer is got")

        return answer.content
