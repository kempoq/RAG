from typing import Any

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    query: str = Field(min_length=1)


class ChatResponse(BaseModel):
    user_query: str
    answer: str
    cypher_query: str
    graph_db_info: list[dict[str, Any]]
    token_usage: int
