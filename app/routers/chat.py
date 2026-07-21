import json
from fastapi import APIRouter, HTTPException

from app.models import ChatRequest, ChatResponse, HistoryItem
from app.rag.retriever import retrieve
from app.rag.generator import generate_answer
from app.database import log_qna, get_history

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        results = retrieve(request.question)
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))

    context_chunks = [r["text"] for r in results]
    sources = sorted({r["source"] for r in results})

    try:
        answer = generate_answer(request.question, context_chunks)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    log_qna(request.question, answer, json.dumps(sources))

    return ChatResponse(answer=answer, sources=sources)


@router.get("/history", response_model=list[HistoryItem])
def history(limit: int = 50):
    return get_history(limit)
