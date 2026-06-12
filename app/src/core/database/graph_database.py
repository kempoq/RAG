import logging
from typing import Any

from langchain_neo4j import Neo4jGraph

from app.src.core.config import env_settings
from app.src.core.database.constants import CONSTRAINTS, SAMPLE_DOCS, UNIQUE_KEYS
from app.src.core.exceptions import GraphDbError

logger = logging.getLogger(__name__)


def get_graph() -> Neo4jGraph:
    """Создаёт подключение к Neo4j"""

    try:
        neo4j_client = Neo4jGraph(
            url=env_settings.neo4j_uri,
            username=env_settings.neo4j_user,
            password=env_settings.neo4j_password.get_secret_value(),
            database=env_settings.neo4j_database,
            refresh_schema=False,
            sanitize=True,
            driver_config={"notifications_min_severity": "WARNING"},
        )
    except Exception as e:
        raise GraphDbError("Connection failed", e)

    return neo4j_client


def create_constraints(graph: Neo4jGraph) -> None:
    """Создаёт ограничения уникальности в Neo4j."""

    for c in CONSTRAINTS:
        graph.query(c)
    logger.info("All constraints are created/approved.")


def load_docs_to_graph(graph: Neo4jGraph, docs: list[dict[str, Any]]) -> None:
    """
    Идемпотентная загрузка документов в граф (MERGE).
    Безопасно запускать повторно — дублей не создаёт.
    """

    for doc in docs:
        # 1. Upsert узла Документ
        graph.query(
            """
            MERGE (d:Документ {doc_id: $doc_id})
            SET d.title = $title, d.source_type = $source_type, d.updated_at = timestamp()
            """,
            doc,
        )

        # 2. Upsert сущностей
        for ent in doc["entities"]:
            label = ent["type"]
            pk = UNIQUE_KEYS[label]
            props = {**ent["props"], "mentioned_in": doc["doc_id"]}
            graph.query(
                f"""
                MERGE (n:{label} {{{pk}: $props.{pk}}})
                SET n += $props
                """,
                {"props": props},
            )

        # 3. Upsert связей
        for rel in doc["relations"]:
            src_type, src_val = rel["source"]
            tgt_type, tgt_val = rel["target"]
            src_pk = UNIQUE_KEYS[src_type]
            tgt_pk = UNIQUE_KEYS[tgt_type]
            graph.query(
                f"""
                MATCH (s:{src_type} {{{src_pk}: $src_val}})
                MATCH (t:{tgt_type} {{{tgt_pk}: $tgt_val}})
                MERGE (s)-[r:{rel["type"]}]->(t)
                SET r += $props, r.source_doc = $source_doc
                """,
                {
                    "src_val": src_val,
                    "tgt_val": tgt_val,
                    "props": rel["props"],
                    "source_doc": doc["doc_id"],
                },
            )

    logger.info(f"Loaded documents: {len(docs)}. Graph is updated incrementally.")


def is_graph_empty(graph: Neo4jGraph) -> bool:
    """Проверяет, есть ли связи в графе"""

    answer = graph.query("MATCH (n) RETURN count(n) AS node_count")

    return answer[0]["node_count"] == 0


def load_graph(graph: Neo4jGraph) -> None:
    """Заполняет граф, если в графе нет связей (начальна загрузка)"""

    try:
        if not is_graph_empty(graph):
            logger.info("Graph isn't empty")
            return

        logger.info("Start filling graph")
        create_constraints(graph)
        load_docs_to_graph(graph, SAMPLE_DOCS)
        logger.info("Graph is filled")
    except Exception as e:
        raise GraphDbError("Error during loading graph", e)
