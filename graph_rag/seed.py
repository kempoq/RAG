"""
seed.py
Первоначальная загрузка тестовых данных в Neo4j.
Запускать один раз: uv run python -m graph_rag.seed
"""

from graph_rag.graph_chain import get_graph
from graph_rag.graph_loader import create_constraints, load_docs_to_graph, print_graph_stats, SAMPLE_DOCS


def main() -> None:
    graph = get_graph()
    print("✅ Подключение к Neo4j установлено.")

    create_constraints(graph)
    load_docs_to_graph(SAMPLE_DOCS, graph)
    print_graph_stats(graph)


if __name__ == "__main__":
    main()
