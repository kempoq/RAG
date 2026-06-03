from pydantic import BaseModel, Field


class GetDocumentsRequest(BaseModel):
    ext: str = Field(max_length=4, default="txt")


class AddDocumentsRequest(GetDocumentsRequest): ...
