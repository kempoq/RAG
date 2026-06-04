from typing import Any

from app.src.api.graph.repository import GraphRagRepository


class GraphRagService:
    def __init__(self, graph_rag_repository: GraphRagRepository) -> None:
        self._gs_repository = graph_rag_repository

    def get_stats(self) -> dict[str, Any]:
        """Возвращает статистику по графу"""

        print("Start getting stats")
        stats = {
            "nodes_count": self._gs_repository.get_nodes_count(),
            "nodes_count_by_types": self._gs_repository.get_nodes_count_by_types(),
            "rels_count": self._gs_repository.get_rels_count(),
            "rels_count_by_types": self._gs_repository.get_rels_count_by_types(),
        }
        print("Stats are got")

        return stats
