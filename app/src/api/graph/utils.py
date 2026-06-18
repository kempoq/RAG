import re
from typing import Any

from langchain_core.messages import BaseMessage


def extract_cypher_from_markdown(text: str) -> str:
    """Извлекает Cypher запрос из MarkDown блока Cypher кода (```cypher ... ```)"""

    pattern = r"```(?:[a-zA-Z]*\n)?(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    if matches:
        return matches[0].strip()

    return text.strip()


def extract_response_data(workflow_state: dict[str, Any]) -> dict[str, Any]:
    """Извлекает нужные для вывода пользователю поля из экземпляра GraphState (контейнер для данных в Graph QA workflow)"""

    res = {
        "user_query": workflow_state["question"],
        "answer": workflow_state["answer"],
        "cypher_query": workflow_state["graph_db_context"]["cypher_query"],
        "graph_db_info": workflow_state["graph_db_context"]["raw_results"],
        "vector_db_info": workflow_state["vector_db_context"]["relevant_data"],
        "token_usage": 0,
    }

    for message in workflow_state["message_history"]:
        message: BaseMessage

        if message.type != "ai":
            continue

        if response_metadata := message.response_metadata:
            if token_usage := response_metadata.get("token_usage"):
                res["token_usage"] += token_usage.get("total_tokens", 0)

    return res


def merge_dicts_one_deep(d1: dict[str, Any], d2: dict[str, Any]) -> dict[str, Any]:
    """Мерджит словари d1 и d2 (только )"""

    result = d1.copy()
    for k, v in d2.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] |= v
        elif k in result and isinstance(result[k], list) and isinstance(v, list):
            result[k].extend(v)
        else:
            result[k] = v

    return result
