from fastapi import APIRouter

from app.src.api.graph.dependencies import GraphRagServiceDep

graph_router = APIRouter(prefix="/graph", tags=["graph_rag"])


@graph_router.get("/store/stats")
def get_stats(graph_rag_service: GraphRagServiceDep):
    """Получение статистики по графу"""

    graph_stats = graph_rag_service.get_stats()

    return graph_stats
