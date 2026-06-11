import logging
from typing import Any

from app.src.api.graph.repository import GraphRagRepository
from app.src.api.graph.workflow import WorkflowGraphFactory
from app.src.core.ml_models import GigaChatClient

logger = logging.getLogger(__name__)


class GraphRagService:
    def __init__(
        self,
        graph_rag_repository: GraphRagRepository,
        llm: GigaChatClient,
        max_fix_retries: int = 2,
    ) -> None:
        self._gs_repository = graph_rag_repository
        self._llm = llm
        self._workflow_graph_factory = WorkflowGraphFactory(
            graph_rag_repository, llm, max_fix_retries
        )

    def get_stats(self) -> dict[str, Any]:
        """Возвращает статистику по графу"""

        logger.info("Start getting stats")
        stats = {
            "nodes_count": self._gs_repository.get_nodes_count(),
            "nodes_count_by_types": self._gs_repository.get_nodes_count_by_types(),
            "rels_count": self._gs_repository.get_rels_count(),
            "rels_count_by_types": self._gs_repository.get_rels_count_by_types(),
        }
        logger.info("Stats are got")

        return stats

    def get_graph_schema(self) -> str:
        """Возвращает схему графа"""

        graph_schema = self._gs_repository.get_graph_schema()

        return graph_schema

    def chat(self, query: str) -> dict[str, Any]:
        """Реализует логику графового RAG"""

        logger.info("Start Graph RAG workflow")
        workflow_graph = self._workflow_graph_factory.create_workflow()
        answer = workflow_graph.invoke({"question": query})
        logger.info("Answer is got")

        return answer
