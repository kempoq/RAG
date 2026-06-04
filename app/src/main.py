from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.src.api.main import api
from app.src.core.database.graph_database import get_graph, load_graph
from app.src.core.ml_models import get_embedding_model_api


@asynccontextmanager
async def lifespan(_app: FastAPI):
    graph_db_conn = get_graph()

    api.state.emb_model = get_embedding_model_api()
    api.state.graph_db = graph_db_conn

    load_graph(graph_db_conn)

    yield

    graph_db_conn.close()
    del graph_db_conn


app = FastAPI(docs_url=None, redoc_url=None, lifespan=lifespan)


app.mount("/api/v1", app=api)
