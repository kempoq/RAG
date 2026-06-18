from typing import Any

from langchain_core.messages import AIMessage


def extract_necessary_message_data(message: AIMessage) -> dict[str, Any]:
    """Извлекает нужные для ответа пользователю данные из AIMessage"""

    response_metadata = message.response_metadata
    model_name = response_metadata.get("model_name", "Model xxx")
    token_usage = response_metadata.get("token_usage", {"total_tokens": -1})

    return {
        "answer": message.content,
        "token_usage": {model_name: token_usage.get("total_tokens", -1)},
    }
