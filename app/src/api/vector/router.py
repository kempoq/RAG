from fastapi import APIRouter

from app.src.api.vector.dependencies import VectorRagServiceDep
from app.src.api.vector.documents.dependencies import DocumentsServiceDep
from app.src.api.vector.schemas import AddDocumentsRequest

vector_router = APIRouter(prefix="/vector", tags=["vector_rag"])


@vector_router.get("/store/docs")
def get_documents(documents_service: DocumentsServiceDep, ext: str):
    filenames = documents_service.get_filenames(ext=ext)

    return {"filenames": filenames}


@vector_router.post("/store/docs")
def add_documents(
    vectore_rag_service: VectorRagServiceDep,
    request_data: AddDocumentsRequest,
):
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
