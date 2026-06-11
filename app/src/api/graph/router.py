from fastapi import APIRouter

from app.src.api.graph.dependencies import GraphRagServiceDep
from app.src.api.graph.schemas import ChatRequest

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


@graph_router.post("/chat")
def chat(graph_rag_service: GraphRagServiceDep, request_data: ChatRequest):
    """Запрос к LLM (графовый RAG)"""

    answer = graph_rag_service.chat(query=request_data.query)

    return {"query": request_data.query, "answer": answer}
