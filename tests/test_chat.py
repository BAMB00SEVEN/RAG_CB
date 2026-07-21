"""
Basic tests. Run with: pytest tests/
Note: test_chat_endpoint requires GROQ_API_KEY to be set and the index to be built,
since it performs a real end-to-end call. The other tests do not need any API key.
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from app.main import app
from app.utils.text_splitter import split_text

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_home_page_served():
    response = client.get("/")
    assert response.status_code == 200


def test_text_splitter_basic():
    text = "a" * 1200
    chunks = split_text(text, chunk_size=500, chunk_overlap=50)
    assert len(chunks) >= 2
    assert all(len(c) <= 500 for c in chunks)


def test_text_splitter_empty():
    assert split_text("", chunk_size=500, chunk_overlap=50) == []


def test_chat_endpoint_requires_question():
    response = client.post("/api/chat", json={"question": ""})
    assert response.status_code == 422  # validation error, empty not allowed
