from typing import Annotated

from fastapi import Depends, Request
from langchain_chroma import Chroma

from app.src.core.config import settings


def get_vector_store(request: Request) -> Chroma:
    return Chroma(
        collection_name=settings.chroma_collection_name,
        embedding_function=request.app.state.emb_model,
        persist_directory=settings.chroma_dir,
    )


VectorStoreDep = Annotated[Chroma, Depends(get_vector_store)]
