from typing import Annotated

from fastapi import APIRouter, Query

from app.src.api.vector.dependencies import VectorRagServiceDep
from app.src.api.vector.documents.dependencies import DocumentsServiceDep
from app.src.api.vector.schemas import AddDocumentsRequest, ChatQuery, GetDocumentsQuery

vector_router = APIRouter(prefix="/vector", tags=["vector_rag"])


@vector_router.get("/store/docs")
def get_documents(
    documents_service: DocumentsServiceDep,
    query_params: Annotated[GetDocumentsQuery, Query()],
):
    """Вывод файлов в директории с указанным расширением"""

    filenames = documents_service.get_filenames(ext=query_params.ext)

    return {"filenames": filenames}


@vector_router.post("/store/docs")
def add_documents(
    vectore_rag_service: VectorRagServiceDep,
    request_data: AddDocumentsRequest,
):
    """Добавление документов в векторную БД"""

    files, ids = vectore_rag_service.add_documents(ext=request_data.ext)

    if ids:
        response = {
            "msg": f"{len(files)} файлов разделены на {len(ids)} документов и загружены в векторную БД",
            "files": files,
            "ids10": ids[:10],
        }
    else:
        response = {
            "msg": "Нет новых новых файлов, документы не были добавлены в БД",
            "files": None,
            "ids10": None,
        }

    return response


@vector_router.get("/chat")
def chat(
    vectore_rag_service: VectorRagServiceDep,
    query_params: Annotated[ChatQuery, Query()],
):
    """Запрос к LLM (RAG)"""

    answer = vectore_rag_service.chat(
        query=query_params.query, docs_count=query_params.docs_count
    )

    return {"query": query_params.query, "answer": answer}
