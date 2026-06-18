from typing import Self

from fastapi import UploadFile
from pydantic import BaseModel, Field, model_validator


class AddDocumentsRequest(BaseModel):
    files: list[UploadFile]

    @model_validator(mode="after")
    def check_files_constraints(self) -> Self:
        for file in self.files:
            if file.size > 50 * 1024 * 1024:
                raise ValueError("File size must be less than 50 MB")
            if file.filename.split(".")[-1] != "txt":
                raise ValueError("Can process only txt files")

        return self


class ChatRequest(BaseModel):
    query: str = Field(min_length=1)
    docs_count: int = Field(ge=3, default=3)
    temperature: float = Field(ge=0.0, le=2.0)


class ChatResponse(BaseModel):
    query: str
    answer: str
    token_usage: dict[str, int]
    relevant_info: list[str]


class GetDocumentsRequest(ChatRequest): ...


class VectorDbInfo(BaseModel):
    total_docs: int
    embedding_model: str
