from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.src.api import api
from app.src.core import (
    configure_logging,
    get_embedding_model_api,
    get_graph,
    load_graph,
)
from app.src.frontend import frontend

configure_logging()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    graph_db_conn = None

    try:
        graph_db_conn = get_graph()
        load_graph(graph_db_conn)
    except:
        ...

    api.state.emb_model = get_embedding_model_api()
    api.state.graph_db = graph_db_conn

    yield

    if graph_db_conn:
        graph_db_conn.close()
        del graph_db_conn


app = FastAPI(docs_url=None, redoc_url=None, lifespan=lifespan)


app.mount("/api/v1", app=api)
app.mount("/", app=frontend)
