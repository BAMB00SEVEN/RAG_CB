from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.database import init_db
from app.routers import chat
from app.config import BASE_DIR


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="RAG Chatbot",
    description="A Retrieval-Augmented Generation chatbot API (FastAPI + FAISS + Groq)",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(chat.router)

STATIC_DIR = BASE_DIR / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
def serve_index():
    return FileResponse(str(STATIC_DIR / "index.html"))


@app.get("/health")
def health_check():
    return {"status": "ok"}
