from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.src.api.main import api
from app.src.core.ml_models import get_embedding_model_api


@asynccontextmanager
async def lifespan(_app: FastAPI):
    api.state.emb_model = get_embedding_model_api()

    yield


app = FastAPI(docs_url=None, redoc_url=None, lifespan=lifespan)


app.mount("/api/v1", app=api)
