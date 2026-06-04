from pydantic import BaseModel, Field


class GetDocumentsQuery(BaseModel):
    ext: str = Field(max_length=4, default="txt")


class AddDocumentsRequest(GetDocumentsQuery): ...


class ChatQuery(BaseModel):
    query: str = Field(min_length=1)
    docs_count: int = Field(ge=3, default=3)
