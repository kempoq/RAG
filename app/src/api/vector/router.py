from typing import Annotated

from fastapi import APIRouter, Form, status
from fastapi.responses import Response

from app.src.api.utils import set_cache_control_headers
from app.src.api.vector.dependencies import (
    VectorRagChatServiceDep,
    VectorRagStorageServiceDep,
)
from app.src.api.vector.schemas import (
    AddDocumentsRequest,
    AddDocumentsResponse,
    ChatRequest,
    ChatResponse,
    GetDocumentsRequest,
    GetFilesResponse,
    GetSimilarDocsResponse,
    GetStorageInfoResponse,
)

vector_router = APIRouter(prefix="/vector", tags=["vector_rag"])


@vector_router.get("/storage/files", response_model=GetFilesResponse)
def get_downloaded_files(
    vectore_rag_service: VectorRagStorageServiceDep, response: Response
) -> GetFilesResponse:
    """Вывод загруженных файлов"""

    files = vectore_rag_service.get_downloaded_files()
    set_cache_control_headers(response)

    return {"files": files}


@vector_router.get("/storage/info", response_model=GetStorageInfoResponse)
def get_storage_info(
    vectore_rag_service: VectorRagStorageServiceDep, response: Response
) -> GetStorageInfoResponse:
    """Общая информация о ChromaDB"""

    storage_info = vectore_rag_service.get_info()
    set_cache_control_headers(response)

    return storage_info


@vector_router.post("/storage/docs", response_model=AddDocumentsResponse)
def add_documents(
    vectore_rag_service: VectorRagStorageServiceDep,
    request_data: Annotated[
        AddDocumentsRequest, Form(..., media_type="multipart/form-data")
    ],
    response: Response,
) -> AddDocumentsResponse:
    """Добавление документов в векторную БД"""

    ids = vectore_rag_service.add_documents(files=request_data.files)

    if ids:
        response_content = {
            "msg": f"{len(ids)} embeddings were inserted in ChromaDB",
            "ids10": ids[:10],
        }
        response.status_code = status.HTTP_201_CREATED
    else:
        response_content = {
            "msg": "No embeddings were inserted in ChromaDB. Chosen files have already been processed",
            "ids10": None,
        }
        response.status_code = status.HTTP_200_OK

    return response_content


@vector_router.post("/storage/search", response_model=GetSimilarDocsResponse)
def get_similar_documents(
    vectore_rag_service: VectorRagStorageServiceDep, request_data: GetDocumentsRequest
) -> GetSimilarDocsResponse:
    """Возвращает документы, наиболее релевантные к запросу"""

    docs = vectore_rag_service.get_documents(
        query=request_data.query, docs_count=request_data.docs_count
    )

    return {"docs": docs}


@vector_router.post("/chat", response_model=ChatResponse)
def chat(
    vectore_rag_chat_service: VectorRagChatServiceDep,
    request_data: ChatRequest,
) -> ChatResponse:
    """Запрос к LLM (RAG)"""

    response = vectore_rag_chat_service.chat(
        query=request_data.query,
        temperature=request_data.temperature,
        docs_count=request_data.docs_count,
    )

    return response
