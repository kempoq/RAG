from typing import Any

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    query: str = Field(min_length=1)
    docs_count: int = Field(ge=3, default=3)
    temperature: float = Field(ge=0.0, le=2.0)


class ChatResponse(BaseModel):
    user_query: str
    answer: str | None
    cypher_query: str
    graph_db_info: list[dict[str, Any]]
    token_usage: dict[str, int]
    vector_db_info: list[str]
