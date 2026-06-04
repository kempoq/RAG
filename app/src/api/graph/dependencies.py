from typing import Annotated

from fastapi import Depends, Request

from app.src.api.graph.repository import GraphRagRepository
from app.src.api.graph.service import GraphRagService
from app.src.core.ml_models import get_llm


def get_graph_rag_service(request: Request) -> GraphRagService:
    graph_rag_repository = GraphRagRepository(graph_db_conn=request.app.state.graph_db)
    llm = get_llm()

    return GraphRagService(graph_rag_repository=graph_rag_repository, llm=llm)


GraphRagServiceDep = Annotated[GraphRagService, Depends(get_graph_rag_service)]
