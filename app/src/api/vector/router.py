from typing import Annotated

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app.src.api.vector.dependencies import VectorRagServiceDep
from app.src.api.vector.schemas import (
    AddDocumentsRequest,
    ChatRequest,
    GetDocumentsQuery,
)

vector_router = APIRouter(prefix="/vector", tags=["vector_rag"])


@vector_router.get("/store/docs")
def get_documents(
    vectore_rag_service: VectorRagServiceDep,
    query_params: Annotated[GetDocumentsQuery, Query()],
):
    """Вывод файлов в директории с указанным расширением"""

    d_files, nd_files = vectore_rag_service.get_filenames(ext=query_params.ext)

    return {"downloaded": d_files, "pending": nd_files}


@vector_router.post("/store/docs")
def add_documents(
    vectore_rag_service: VectorRagServiceDep,
    request_data: AddDocumentsRequest,
):
    """Добавление документов в векторную БД"""

    files, ids = vectore_rag_service.add_documents(ext=request_data.ext)

    if ids:
        response = JSONResponse(
            content={
                "msg": f"{len(files)} файлов разделены на {len(ids)} документов и загружены в векторную БД",
                "files": files,
                "ids10": ids[:10],
            },
            status_code=201,
        )
    else:
        response = JSONResponse(
            content={
                "msg": "Нет новых новых файлов, документы не были добавлены в БД",
                "files": None,
                "ids10": None,
            },
            status_code=200,
        )

    return response


@vector_router.post("/chat")
def chat(
    vectore_rag_service: VectorRagServiceDep,
    request_data: ChatRequest,
):
    """Запрос к LLM (RAG)"""

    answer = vectore_rag_service.chat(
        query=request_data.query, docs_count=request_data.docs_count
    )

    return {"query": request_data.query, "answer": answer}
