from typing import Annotated

from fastapi import Depends

from app.src.api.vector.documents.dependencies import DocumentsServiceDep
from app.src.api.vector.service import VectorRagChatService, VectorRagService
from app.src.core.database.vector_database import VectorStoreDep
from app.src.core.ml_models import get_llm


def get_vector_rag_service(
    documents_service: DocumentsServiceDep, vector_store: VectorStoreDep
) -> VectorRagService:
    return VectorRagService(
        documents_service=documents_service, vector_store=vector_store
    )


def get_vector_rag_chat_service(vector_store: VectorStoreDep) -> VectorRagChatService:
    return VectorRagChatService(vector_store=vector_store, llm=get_llm())


VectorRagServiceDep = Annotated[VectorRagService, Depends(get_vector_rag_service)]
VectorRagChatServiceDep = Annotated[
    VectorRagChatService, Depends(get_vector_rag_chat_service)
]
