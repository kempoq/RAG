from fastapi import FastAPI

from app.src.api.graph.router import graph_router
from app.src.api.vector.router import vector_router

api = FastAPI(title="RAG test", root_path="/api/v1")

api.include_router(vector_router)
api.include_router(graph_router)


@api.get("/health")
async def health_check():
    return {"status": "healthy"}
