from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    embedding_model_name: str = "deepvk/USER-bge-m3"
    chroma_collection_name: str = "rag"
    chroma_dir: str = ".chroma"
    logging_conf_path: str = "logging_conf.yaml"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    embedding_base_url: str = "http://127.0.0.1:1234/v1"
    embedding_model_name: str = "text-embedding-nomic-embed-text-v1.5"
    static_dir: str = "app/src/frontend/static"
    templates_dir: str = "app/src/frontend/templates"

    llm_base_url: str = "https://xxx"
    llm_model: str = "GigaChat-2"
    auth_base_url: str = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"


class EnvSettings(BaseSettings):
    neo4j_uri: str
    neo4j_user: str
    neo4j_password: SecretStr
    neo4j_database: str
    openai_api_key: str
    embedding_model_api_key: str
    giga_auth_token: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf8", extra="ignore"
    )


settings = Settings()
env_settings = EnvSettings()
