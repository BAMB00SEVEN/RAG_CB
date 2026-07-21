"""
Central place for all configuration/settings.
Reads values from environment variables (loaded from .env in local dev).
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
TOP_K = int(os.getenv("TOP_K", "4"))

DOCS_DIR = BASE_DIR / "data" / "docs"
INDEX_DIR = BASE_DIR / "data" / "faiss_index"
INDEX_FILE = INDEX_DIR / "index.faiss"
METADATA_FILE = INDEX_DIR / "metadata.json"

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./qna.db")

CHUNK_SIZE = 500       # characters per chunk
CHUNK_OVERLAP = 80     # overlap between consecutive chunks
