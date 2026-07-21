from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]


class HistoryItem(BaseModel):
    id: int
    question: str
    answer: str
    sources: str
    created_at: str
