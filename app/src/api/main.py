from fastapi import FastAPI

from app.src.api.vector.router import vector_router

api = FastAPI(title="RAG test", root_path="/api/v1")

api.include_router(vector_router)


@api.get("/health")
async def health_check():
    return {"status": "healthy"}
