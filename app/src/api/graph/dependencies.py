from typing import Annotated

from fastapi import Depends, Request

from app.src.api.graph.repository import GraphRagRepository
from app.src.api.graph.service import GraphRagService
from app.src.api.graph.workflow import WorkflowGraphFactory
from app.src.api.vector.dependencies import VectorRagStorageServiceDep


def get_graph_rag_service(
    request: Request, vector_rag_storage_service: VectorRagStorageServiceDep
) -> GraphRagService:
    graph_rag_repository = GraphRagRepository(graph_db_conn=request.app.state.graph_db)
    workflow_factory = WorkflowGraphFactory(
        graph_rag_repository=graph_rag_repository,
        vector_rag_storage_service=vector_rag_storage_service,
        chat_llm=request.app.state.llm,
        cypher_generating_llm=request.app.state.llm,
        max_fix_retries=2,
    )

    return GraphRagService(
        graph_rag_repository=graph_rag_repository,
        workflow_factory=workflow_factory,
        llm=request.app.state.llm,
    )


GraphRagServiceDep = Annotated[GraphRagService, Depends(get_graph_rag_service)]
