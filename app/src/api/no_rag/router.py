from fastapi import APIRouter

from app.src.api.no_rag.dependencies import NoRagServiceDep
from app.src.api.no_rag.schemas import ChatRequest, ChatResponse

no_rag_router = APIRouter(prefix="/no-rag", tags=["no rag"])


@no_rag_router.post("/chat", response_model=ChatResponse)
def chat(no_rag_service: NoRagServiceDep, request_data: ChatRequest) -> ChatResponse:
    """Отправка запросов в LLM"""

    answer = no_rag_service.chat(query=request_data.query)

    return {"answer": answer}
