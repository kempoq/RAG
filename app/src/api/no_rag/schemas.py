from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    query: str
    temperature: float = Field(ge=0.0, le=2.0)


class ChatResponse(BaseModel):
    query: str
    answer: str
    token_usage: dict[str, int]
