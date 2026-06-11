from typing import Annotated

from fastapi import Depends
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.src.api.vector.documents.service import DocumentsService
from app.src.core.config import settings


def get_text_splitter() -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        add_start_index=True,
    )


TextSplitterDep = Annotated[RecursiveCharacterTextSplitter, Depends(get_text_splitter)]


def get_documents_service(text_splitter: TextSplitterDep) -> DocumentsService:
    return DocumentsService(
        text_splitter=text_splitter,
        dir=settings.files_dir,
    )


DocumentsServiceDep = Annotated[DocumentsService, Depends(get_documents_service)]
