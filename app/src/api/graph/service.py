from functools import partial
from typing import Any

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_gigachat.chat_models import GigaChat
from langchain_neo4j import GraphCypherQAChain

from app.src.api.graph.constants import (
    FIX_CYPHER_TEMPLATE,
    GENERATE_CYPHER_TEMPLATE,
    PROMPT_TEMPLATE,
)
from app.src.api.graph.repository import GraphRagRepository
from app.src.api.graph.utlis import extract_cypher_from_markdown


class GraphRagService:
    def __init__(self, graph_rag_repository: GraphRagRepository, llm: GigaChat) -> None:
        self._gs_repository = graph_rag_repository
        self._llm = llm

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

    def get_graph_schema(self) -> str:
        """Возвращает схему графа"""

        graph_schema = self._gs_repository.get_graph_schema()

        return graph_schema

    def _generate_cypher_query(
        self, inputs: dict[str, Any], max_retries: int, **_: dict[Any, Any]
    ) -> str:
        """
        Генерирует Cypher запрос на основе вопроса. Если есть ошибка в синтаксисе,
        то генерирует заново с учетом ошибки
        """

        result_prompt = None
        retry_count = 0

        while True:
            if result_prompt is None:
                result_prompt = GENERATE_CYPHER_TEMPLATE.format(
                    schema=inputs["schema"], question=inputs["question"]
                )
            cypher_query = extract_cypher_from_markdown(
                self._llm.invoke(result_prompt).content
            )

            try:
                self._gs_repository.explain_query(cypher_query)
                return cypher_query
            except Exception as e:
                error_msg = str(e)
                print(
                    f"Attempt {retry_count + 1} is unsuccessfull. Error: {error_msg[:100]}"
                )

                if retry_count == max_retries:
                    raise e

                result_prompt = FIX_CYPHER_TEMPLATE.format(
                    error_msg=error_msg,
                    schema=inputs["schema"],
                    question=inputs["question"],
                    cypher=cypher_query,
                )
                retry_count += 1

    def _init_qa_chain(
        self, max_query_generation_retries: int = 2
    ) -> GraphCypherQAChain:
        """Инициализирует цепочку для ответа на вопросы по графу"""

        print("Start initializing QA-chain")
        qa_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=PROMPT_TEMPLATE,
        )

        qa_chain = qa_prompt | self._llm | StrOutputParser()
        cypher_generation_chain = RunnableLambda(
            partial(
                self._generate_cypher_query, max_retries=max_query_generation_retries
            )
        )

        chain = GraphCypherQAChain(
            graph=self._gs_repository.graph_db_conn,
            graph_schema=self._gs_repository.get_graph_schema(),
            cypher_generation_chain=cypher_generation_chain,
            qa_chain=qa_chain,
            verbose=True,
            validate_cypher=True,
            allow_dangerous_requests=True,
            return_intermediate_steps=True,
        )
        print("QA-chain is initialized")

        return chain

    def chat(self, query: str) -> str:
        """Реализует логику графового RAG"""

        print("Start querying LLM with Graph DB")
        qa_chain = self._init_qa_chain()
        answer = qa_chain.invoke({"query": query})
        print(answer["intermediate_steps"])
        print("Answer is got")

        return answer.get("result", "")
