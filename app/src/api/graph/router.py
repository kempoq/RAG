from fastapi import APIRouter

from app.src.api.graph.dependencies import GraphRagServiceDep
from app.src.api.graph.schemas import ChatRequest, ChatResponse

graph_router = APIRouter(prefix="/graph", tags=["graph_rag"])


@graph_router.get("/store/stats")
def get_stats(graph_rag_service: GraphRagServiceDep):
    """Получение статистики по графу"""

    graph_stats = graph_rag_service.get_stats()

    return graph_stats


@graph_router.get("/store/schema")
def get_graph_schema(graph_rag_service: GraphRagServiceDep):
    """Получение схемы графа"""

    graph_schema = graph_rag_service.get_graph_schema()

    return {"schema": graph_schema}


@graph_router.post("/chat", response_model=ChatResponse)
def chat(
    graph_rag_service: GraphRagServiceDep, request_data: ChatRequest
) -> ChatResponse:
    """Запрос к LLM (графовый RAG)"""

    response = graph_rag_service.chat(
        query=request_data.query,
        temperature=request_data.temperature,
        docs_count=request_data.docs_count,
    )

    return response
