from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

from app.src.api.graph.router import graph_router
from app.src.api.no_rag.router import no_rag_router
from app.src.api.vector.router import vector_router

api = FastAPI(title="RAG test", root_path="/api/v1")

api.include_router(vector_router)
api.include_router(graph_router)
api.include_router(no_rag_router)

api.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=5)


@api.get("/health")
async def health_check():
    return {"status": "healthy"}
