from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.src.api import api
from app.src.core import (
    configure_logging,
    get_embedding_model_api,
    get_graph,
    get_llm,
    load_graph,
)
from app.src.frontend import frontend

configure_logging()


@asynccontextmanager
async def lifespan(_app: FastAPI):

    api.state.emb_model = get_embedding_model_api()
    api.state.graph_db = get_graph()
    api.state.llm = get_llm()

    load_graph(api.state.graph_db)

    yield

    api.state.graph_db.close()


app = FastAPI(docs_url=None, redoc_url=None, lifespan=lifespan)


app.mount("/api/v1", app=api)
app.mount("/", app=frontend)
