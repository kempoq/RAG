import logging
from typing import Any

import requests
from gigachat.exceptions import AuthenticationError
from langchain_core.language_models.chat_models import _ChatModelBinding
from langchain_core.messages import AIMessage
from langchain_gigachat.chat_models import GigaChat

# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from app.src.core.config import env_settings, settings

logger = logging.getLogger(__name__)

# def get_embedding_model_hf() -> HuggingFaceEmbeddings:
#     logger.info("Start downloading embedding model")
#     embedding_model = HuggingFaceEmbeddings(
#         model_name="placeholder",
#         model_kwargs={"device": "cpu"},
#         encode_kwargs={"normalize_embeddings": True},
#     )
#     logger.info("Embedding model is downloaded")
#     return embedding_model


def get_embedding_model_api() -> OpenAIEmbeddings:
    logger.info("Start downloading embedding model")
    embedding_model = OpenAIEmbeddings(
        model=settings.embedding_model_name,
        base_url=settings.embedding_base_url,
        check_embedding_ctx_length=False,
        openai_api_key=env_settings.embedding_model_api_key,
    )
    logger.info("Embedding model is downloaded")
    return embedding_model


class GigaChatClient:
    def __init__(
        self, model: str, max_auth_retries: int = 2, verify_ssl: bool = True
    ) -> None:
        self._model = model
        self._max_auth_retries = max_auth_retries
        self._verify_ssl = verify_ssl
        self._set_access_token()
        self._set_gigachat_client()

    @property
    def client(self) -> GigaChat:
        return self._client

    def _set_access_token(self) -> str:
        """Возвращает Access Token для авторизации в API GigaChat"""

        logger.debug("Start getting access token")
        payload = {"scope": "GIGACHAT_API_PERS"}
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": "bca582b8-e12f-47a4-a3c6-730bc28f4422",
            "Authorization": f"Basic {env_settings.giga_auth_token}",
        }

        response = requests.request(
            method="POST",
            url=settings.auth_base_url,
            headers=headers,
            data=payload,
            verify=self._verify_ssl,
        )
        response.raise_for_status()

        self._access_token = response.json()["access_token"]
        logger.debug("Access token is got")

    def _set_gigachat_client(self) -> GigaChat:
        """Возвращает клиент для взаимодействия с LLM GigaChat"""

        self._client = GigaChat(
            model=self._model,
            access_token=self._access_token,
            verify_ssl_certs=self._verify_ssl,
            temperature=0.0,
        )

    def get_model_with_new_settings(
        self, **kwargs: dict[str, Any]
    ) -> _ChatModelBinding:
        """Устанавливает параметры модели. Обертка над методом GigaChat.bind(...)"""

        logger.debug(
            f"Returning model with params: {', '.join([f'{k}={v}' for k, v in kwargs.items()])}"
        )
        return self._client.bind(**kwargs)

    def invoke(self, *args: list[Any], **kwargs: dict[str, Any]) -> AIMessage:
        """Отправляет запрос к LLM"""

        retry_count = 0

        while True:
            try:
                return self._client.invoke(*args, **kwargs)
            except AuthenticationError as ae:
                logger.info("Access token is expired, trying to refresh it")
                if retry_count == self._max_auth_retries:
                    raise ae
                self._set_access_token()
                self._set_gigachat_client()

                retry_count += 1


def get_gigachat_client() -> GigaChatClient:
    """Возвращает клиент для взаимодействия с GigaChat"""

    logger.info("Start initializing GigaChat client")
    giga_client = GigaChatClient(model=settings.chat_llm_model)
    logger.info("GigaChat client is initialized")

    return giga_client


def get_openai_llm_client() -> ChatOpenAI:
    """Возвращает клиент для взаимодействия с LLM с API стандарта OpenAI"""

    logger.info("Start initializing OpenAI based LLM client")
    llm = ChatOpenAI(
        model=settings.cypher_llm_model,
        base_url=settings.cypher_llm_base_url,
        api_key=env_settings.groq_api_key,
        temperature=0,
    )
    logger.info("LLM client is initialized")

    return llm
