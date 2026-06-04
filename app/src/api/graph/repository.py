from langchain_neo4j import Neo4jGraph


class GraphRagRepository:
    def __init__(self, graph_db_conn: Neo4jGraph) -> None:
        self._graph_db_conn = graph_db_conn

    @property
    def graph_db_conn(self) -> Neo4jGraph:
        return self._graph_db_conn

    def get_nodes_count(self) -> int:
        """Возвращает количество узлов"""

        query = "MATCH (n) RETURN count(n) as total_nodes"
        res = self._graph_db_conn.query(query)

        return res[0]["total_nodes"]

    def get_nodes_count_by_types(self) -> dict[str, int]:
        """Возвращает количество узлов по их типам"""

        query = "MATCH (n) RETURN labels(n)[0] as label, count(n) as count ORDER BY count DESC"
        res = self._graph_db_conn.query(query)

        return {row["label"]: row["count"] for row in res}

    def get_rels_count(self) -> int:
        """Возвращает количество связей"""

        query = "MATCH ()-[r]->() RETURN count(r) as total_rels"
        res = self._graph_db_conn.query(query)

        return res[0]["total_rels"]

    def get_rels_count_by_types(self) -> dict[str, int]:
        """Возвращает количество связей по их типам"""

        query = "MATCH ()-[r]->() RETURN type(r) as rel_type, count(r) as count ORDER BY count DESC"
        res = self._graph_db_conn.query(query)

        return {row["rel_type"]: row["count"] for row in res}

    def get_graph_schema(self) -> str:
        """Возвращает схему графа"""

        self._graph_db_conn.refresh_schema()

        return self._graph_db_conn.get_schema

    def explain_query(self, query: str) -> None:
        """
        Запускается запрос с EXPLAIN в начале. В итоге строится план запроса без получения данных.
        Используется для проверки синтаксиса
        """

        self._graph_db_conn.query(f"EXPLAIN {query}")
