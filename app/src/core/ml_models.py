from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings

from app.src.core.config import env_settings, settings


def get_embedding_model_hf() -> HuggingFaceEmbeddings:
    print("Start downloading embedding model")
    embedding_model = HuggingFaceEmbeddings(
        model_name="placeholder",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    print("Embedding model is downloaded")
    return embedding_model


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
