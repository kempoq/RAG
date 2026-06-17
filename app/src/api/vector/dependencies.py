from typing import Annotated

from fastapi import Depends, Request

from app.src.api.vector.documents.dependencies import DocumentsServiceDep
from app.src.api.vector.service import VectorRagChatService, VectorRagStorageService
from app.src.core.database.vector_database import VectorStoreDep


def get_vector_rag_storage_service(
    documents_service: DocumentsServiceDep, vector_store: VectorStoreDep
) -> VectorRagStorageService:
    return VectorRagStorageService(
        documents_service=documents_service, vector_store=vector_store
    )


def get_vector_rag_chat_service(
    request: Request, vector_store: VectorStoreDep
) -> VectorRagChatService:
    return VectorRagChatService(vector_store=vector_store, llm=request.app.state.llm)


VectorRagStorageServiceDep = Annotated[
    VectorRagStorageService, Depends(get_vector_rag_storage_service)
]
VectorRagChatServiceDep = Annotated[
    VectorRagChatService, Depends(get_vector_rag_chat_service)
]
