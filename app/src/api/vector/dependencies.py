from typing import Annotated

from fastapi import Depends

from app.src.api.vector.documents.dependencies import DocumentsServiceDep
from app.src.api.vector.service import VectorRagService
from app.src.core.database.vector_database import VectorStoreDep


def get_vector_rag_service(
    documents_service: DocumentsServiceDep, vector_store: VectorStoreDep
) -> VectorRagService:
    return VectorRagService(
        documents_service=documents_service,
        vector_store=vector_store,
    )


VectorRagServiceDep = Annotated[VectorRagService, Depends(get_vector_rag_service)]
