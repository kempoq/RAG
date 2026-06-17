from typing import Annotated

from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse

from app.src.api.vector.dependencies import (
    VectorRagChatServiceDep,
    VectorRagStorageServiceDep,
)
from app.src.api.vector.schemas import (
    AddDocumentsRequest,
    ChatRequest,
    GetDocumentsRequest,
)

vector_router = APIRouter(prefix="/vector", tags=["vector_rag"])


@vector_router.get("/storage/files")
def get_downloaded_files(vectore_rag_service: VectorRagStorageServiceDep):
    """Вывод загруженных файлов"""

    files = vectore_rag_service.get_downloaded_files()

    return {"files": files}


@vector_router.get("/storage/info")
def get_storage_info(vectore_rag_service: VectorRagStorageServiceDep):
    storage_info = vectore_rag_service.get_info()

    return storage_info


@vector_router.post("/storage/docs")
def add_documents(
    vectore_rag_service: VectorRagStorageServiceDep,
    request_data: Annotated[
        AddDocumentsRequest, Form(..., media_type="multipart/form-data")
    ],
):
    """Добавление документов в векторную БД"""

    ids = vectore_rag_service.add_documents(files=request_data.files)

    if ids:
        response = JSONResponse(
            content={
                "msg": f"В векторную БД загружено {len(ids)} документов",
                "ids10": ids[:10],
            },
            status_code=201,
        )
    else:
        response = JSONResponse(
            content={
                "msg": "Документы не были загружены в БД",
                "ids10": None,
            },
            status_code=200,
        )

    return response


@vector_router.post("/storage/search")
def get_similar_documents(
    vectore_rag_service: VectorRagStorageServiceDep, request_data: GetDocumentsRequest
):
    """Возвращает документы, наиболее релевантные к запросу"""

    docs = vectore_rag_service.get_documents(
        query=request_data.query, docs_count=request_data.docs_count
    )

    return {"docs": docs}


@vector_router.post("/chat")
def chat(
    vectore_rag_chat_service: VectorRagChatServiceDep,
    request_data: ChatRequest,
):
    """Запрос к LLM (RAG)"""

    answer, relevant_info = vectore_rag_chat_service.chat(
        query=request_data.query, docs_count=request_data.docs_count
    )

    return {
        "query": request_data.query,
        "relevant_info": relevant_info,
        "answer": answer,
    }
