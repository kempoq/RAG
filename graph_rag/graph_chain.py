"""
graph_chain.py
Подключение к Neo4j и GraphCypherQAChain для вопросно-ответной работы с графом.
"""

import os
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph, GraphCypherQAChain
from langchain_openai import ChatOpenAI

load_dotenv()


def get_graph() -> Neo4jGraph:
    """Создаёт подключение к Neo4j из переменных окружения."""
    return Neo4jGraph(
        url=os.environ["NEO4J_URI"],
        username=os.environ["NEO4J_USER"],
        password=os.environ["NEO4J_PASSWORD"],
        database=os.environ.get("NEO4J_DATABASE", "neo4j"),
        refresh_schema=False,
    )


def get_chain(graph: Neo4jGraph, model: str = "gpt-4o-mini", verbose: bool = True) -> GraphCypherQAChain:
    """Создаёт GraphCypherQAChain поверх графа."""
    llm = ChatOpenAI(
        model=model,
        temperature=0,
        openai_api_key=os.environ["OPENAI_API_KEY"],
    )
    return GraphCypherQAChain.from_llm(
        llm=llm,
        graph=graph,
        verbose=verbose,
        allow_dangerous_requests=True,
    )


def ask(chain: GraphCypherQAChain, question: str) -> str:
    """Задаёт вопрос графу и возвращает ответ."""
    result = chain.invoke({"query": question})
    return result.get("result", "")


# ---------------------------------------------------------------------------
# Демонстрационный запуск
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    graph = get_graph()
    print("✅ Подключение к Neo4j установлено.")

    # Обновляем схему один раз перед запросами
    graph.refresh_schema()

    chain = get_chain(graph)

    questions = [
        "Какие реагенты используются при кислотном выщелачивании?",
        "На каком оборудовании проводится ионный обмен?",
        "Какие заводы используют кучное выщелачивание?",
        "Какой параметр критически влияет на химическое осаждение?",
    ]

    for q in questions:
        print(f"\n❓ {q}")
        print(f"💬 {ask(chain, q)}")
