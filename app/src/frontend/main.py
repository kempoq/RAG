from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.src.core.config import settings

frontend = FastAPI(docs_url=None, redoc_url=None)
frontend.mount("/static", StaticFiles(directory=settings.static_dir), name="static")
templates = Jinja2Templates(directory=settings.templates_dir)


@frontend.get("/embedding")
async def embedding_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="emb_page.html")


@frontend.get("/simple-rag")
async def simple_rag_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="simple_rag.html")


@frontend.get("/graph-rag")
async def graph_rag_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="graph_rag.html")
