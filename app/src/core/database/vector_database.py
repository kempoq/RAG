from typing import Annotated

from fastapi import Depends, Request
from langchain_chroma import Chroma

from app.src.core.config import settings
from app.src.core.exceptions import VectoreDbError


def get_vector_store(request: Request) -> Chroma:
    """Возврщает клиент для взаимодействия с ChromaDB"""

    try:
        chroma_client = Chroma(
            collection_name=settings.chroma_collection_name,
            embedding_function=request.app.state.emb_model,
            persist_directory=settings.chroma_dir,
        )
    except Exception as e:
        raise VectoreDbError("Initialization failed", e)

    return chroma_client


VectorStoreDep = Annotated[Chroma, Depends(get_vector_store)]
