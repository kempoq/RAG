from typing import Annotated

from fastapi import Depends, Request

from app.src.api.no_rag.service import NoRagService


def get_no_rag_service(request: Request) -> NoRagService:
    return NoRagService(llm=request.app.state.chat_llm)


NoRagServiceDep = Annotated[NoRagService, Depends(get_no_rag_service)]
