import requests
from langchain_gigachat.chat_models import GigaChat

# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings

from app.src.core.config import env_settings, settings

# def get_embedding_model_hf() -> HuggingFaceEmbeddings:
#     print("Start downloading embedding model")
#     embedding_model = HuggingFaceEmbeddings(
#         model_name="placeholder",
#         model_kwargs={"device": "cpu"},
#         encode_kwargs={"normalize_embeddings": True},
#     )
#     print("Embedding model is downloaded")
#     return embedding_model


def get_embedding_model_api() -> OpenAIEmbeddings:
    print("Start downloading embedding model")
    embedding_model = OpenAIEmbeddings(
        model=settings.embedding_model_name,
        base_url=settings.embedding_base_url,
        check_embedding_ctx_length=False,
        openai_api_key=env_settings.embedding_model_api_key,
    )
    print("Embedding model is downloaded")
    return embedding_model


class GigaChatClient:
    def __init__(self, model: str, oauth_base_url: str, oauth_token: str) -> None:
        self._client = self._init_gigachat(model, oauth_base_url, oauth_token)

    @property
    def client(self) -> GigaChat:
        return self._client

    def _get_access_token(self, oauth_base_url: str, oauth_token: str) -> str:
        """Возвращает Access Token для авторизации в API GigaChat"""

        payload = {"scope": "GIGACHAT_API_PERS"}
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": "bca582b8-e12f-47a4-a3c6-730bc28f4422",
            "Authorization": f"Basic {oauth_token}",
        }

        response = requests.request(
            method="POST",
            url=oauth_base_url,
            headers=headers,
            data=payload,
            verify=True,
        )
        response.raise_for_status()

        return response.json()["access_token"]

    def _init_gigachat(
        self, model: str, oauth_base_url: str, oauth_token: str
    ) -> GigaChat:
        """Возвращает клиент для взаимодействия с LLM GigaChat"""

        access_token = self._get_access_token(oauth_base_url, oauth_token)

        return GigaChat(
            model=model,
            access_token=access_token,
            verify_ssl_certs=True,
        )


def get_llm() -> GigaChat:
    """Возвращает клиент для взаимодействия с LLM моделью"""

    return GigaChatClient(
        model=settings.llm_model,
        oauth_base_url=settings.auth_base_url,
        oauth_token=env_settings.giga_auth_token,
    ).client


# def get_llm() -> ChatOpenAI:
#     """Возвращает клиент для взаимодействия с LLM моделью"""

#     return ChatOpenAI(
#         base_url=settings.llm_base_url,
#         model=settings.llm_model,
#         temperature=0,
#         openai_api_key=env_settings.openai_api_key,
#         timeout=30,
#     )
