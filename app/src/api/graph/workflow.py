import logging
from typing import Any, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph
from neo4j.exceptions import CypherSyntaxError, Neo4jError

from app.src.api.graph.constants import (
    CHAT_PROMPT,
    EXAMPLES,
    FIX_CYPHER_QUERY,
    GENERATE_CYPHER_QUERY,
)
from app.src.api.graph.repository import GraphRagRepository
from app.src.api.graph.utils import extract_cypher_from_markdown
from app.src.core.exceptions import WorkflowGenerationError
from app.src.core.ml_models import GigaChatClient

logger = logging.getLogger(__name__)


class CypherContext(TypedDict):
    schema: str
    examples: list[str]
    question: str


class DatabaseContext(TypedDict):
    cypher_query: str | None
    raw_results: list[dict[str, Any]]
    errors: list[str]
    warnings: list[str]
    retry_count: int


class GraphState(TypedDict):
    question: str
    cypher_context: CypherContext
    database_context: DatabaseContext
    message_history: list[BaseMessage]
    answer: str | None


class WorkflowGraphFactory:
    def __init__(
        self,
        graph_rag_repository: GraphRagRepository,
        llm: GigaChatClient,
        max_fix_retries: int,
    ) -> None:
        self._gr_repository = graph_rag_repository
        self._llm = llm
        self._max_fix_retries = max_fix_retries

    def _init_context(self, state: GraphState) -> GraphState:
        """Инициализация контекста"""

        logger.info("Initializing context")
        graph_schema = self._gr_repository.get_graph_schema()

        return {
            **state,
            "cypher_context": {
                "schema": graph_schema,
                "examples": EXAMPLES,
                "question": state["question"],
            },
            "database_context": {
                "cypher_query": None,
                "raw_results": [],
                "errors": [],
                "warnings": [],
                "retry_count": 0,
            },
            "message_history": [HumanMessage(content=state["question"])],
            "answer": None,
        }

    def _generate_cypher_query(self, state: GraphState) -> GraphState:
        """Генерация Cypher запроса"""

        logger.info("Generating Cypher Query")
        db_ctx = state["database_context"]

        if len(db_ctx["errors"]) != 0 or len(db_ctx["warnings"]) != 0:
            prompt = ChatPromptTemplate.from_messages(FIX_CYPHER_QUERY)
            chain = prompt | RunnableLambda(self._llm.invoke)
            response = chain.invoke(
                {
                    "schema": state["cypher_context"]["schema"],
                    "examples": "\n".join(state["cypher_context"]["examples"]),
                    "query": db_ctx["cypher_query"],
                    "error": db_ctx["errors"][-1] if db_ctx["errors"] else "нет",
                    "warning": db_ctx["warnings"][-1] if db_ctx["warnings"] else "нет",
                    "question": state["cypher_context"]["question"],
                }
            )
            db_ctx["errors"].clear()
            db_ctx["warnings"].clear()
        else:
            prompt = ChatPromptTemplate.from_messages(GENERATE_CYPHER_QUERY)
            chain = prompt | RunnableLambda(self._llm.invoke)
            response = chain.invoke(
                {
                    "schema": state["cypher_context"]["schema"],
                    "examples": "\n".join(state["cypher_context"]["examples"]),
                    "question": state["cypher_context"]["question"],
                }
            )

        cypher = extract_cypher_from_markdown(response.content)

        db_ctx["cypher_query"] = cypher
        state["message_history"].append(response)

        return {
            **state,
            "database_context": db_ctx,
        }

    def _check_query(self, state: GraphState) -> GraphState:
        """Проверка правильности синтаксиса"""

        logger.info("Making query syntax check")
        db_ctx = state["database_context"]

        try:
            warnings = self._gr_repository.check_query(db_ctx["cypher_query"])
            if warnings:
                db_ctx["warnings"].extend(warnings)
                db_ctx["retry_count"] += 1
        except CypherSyntaxError as cse:
            error_msg = str(cse)
            logger.warning(
                f"Cypher query is incorrect. Trying to fix error ({db_ctx['retry_count'] + 1} retry). Syntax error: {error_msg[:50]}"
            )
            db_ctx["errors"].append(error_msg)
            db_ctx["retry_count"] += 1

            state["message_history"].append(
                AIMessage(
                    content=f"Синтаксическая ошибка: {db_ctx['errors'][-1][:200]}... . Попытка исправить."
                )
            )

        return {
            **state,
            "database_context": db_ctx,
        }

    def _execute_query(self, state: GraphState) -> GraphState:
        """Выполнение Cypher запроса"""

        logger.info("Executing Cypher query")
        db_ctx = state["database_context"]

        try:
            results = self._gr_repository.graph_db_conn.query(db_ctx["cypher_query"])
            db_ctx["raw_results"] = results
        except Neo4jError as ne:
            db_ctx["errors"].append(str(ne))
            state["message_history"].append(
                AIMessage(
                    content=f"Результат БД - {len(db_ctx['raw_results'])} записей, ошибка: {db_ctx['errors'][-1][:50]}"
                )
            )

        return {
            **state,
            "database_context": db_ctx,
        }

    def _generate_answer(self, state: GraphState) -> GraphState:
        """Генерация ответа"""

        logger.info("Generating answer")
        raw_results = state["database_context"]["raw_results"]

        prompt = ChatPromptTemplate.from_messages(CHAT_PROMPT)
        chain = prompt | RunnableLambda(self._llm.invoke)
        response = chain.invoke(
            {
                "question": state["question"],
                "context": (
                    str(raw_results)
                    if raw_results
                    else "В базе нет данных для ответа. Отвечай на основе своих знаний"
                ),
            }
        )
        answer = response.content

        state["message_history"].append(AIMessage(content=answer))

        return {
            **state,
            "answer": answer,
        }

    def create_workflow(self) -> CompiledStateGraph:
        """Создания Workflow"""

        def define_path(state: GraphState) -> str:
            """Возвращает статус, на основе которого будет определено дальнейшее движении по графу"""

            if (
                not state["database_context"]["errors"]
                and not state["database_context"]["warnings"]
            ):
                logger.debug("There are no errors/warnings. Going forward")
                return "success"
            elif state["database_context"]["retry_count"] < self._max_fix_retries:
                logger.debug("There are errors/warnings. Go to generate_cypher_query")
                return "retry"
            else:
                logger.debug("Retry count reached limit. Workflow go to end")
                return "failed"

        logger.debug("Start generating and compiling workflow for GraphRAG")
        workflow = StateGraph(state_schema=GraphState)

        workflow.add_node("init_context", self._init_context)
        workflow.add_node("generate_cypher_query", self._generate_cypher_query)
        workflow.add_node("check_query", self._check_query)
        workflow.add_node("execute_query", self._execute_query)
        workflow.add_node("generate_answer", self._generate_answer)

        workflow.set_entry_point("init_context")
        workflow.add_edge("init_context", "generate_cypher_query")
        workflow.add_edge("generate_cypher_query", "check_query")
        workflow.add_conditional_edges(
            "check_query",
            define_path,
            {
                "success": "execute_query",
                "retry": "generate_cypher_query",
                "failed": END,
            },
        )
        workflow.add_edge("execute_query", "generate_answer")
        workflow.add_edge("generate_answer", END)

        try:
            compiled_graph = workflow.compile()
        except Exception as e:
            raise WorkflowGenerationError(
                "Error during generating Graph RAG workflow", e
            )

        logger.debug("Workflow is generated")
        return compiled_graph
