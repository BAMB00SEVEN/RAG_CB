"""
Very small, dependency-light SQLite database layer.
Stores every question + answer pair for history/logging.
"""
import sqlite3
import datetime
from pathlib import Path
from app.config import DATABASE_URL

# DATABASE_URL looks like: sqlite:///./qna.db -> extract the file path
_DB_PATH = DATABASE_URL.replace("sqlite:///", "")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create the qna_logs table if it doesn't already exist."""
    Path(_DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS qna_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            sources TEXT,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def log_qna(question: str, answer: str, sources: str) -> None:
    conn = get_connection()
    conn.execute(
        "INSERT INTO qna_logs (question, answer, sources, created_at) VALUES (?, ?, ?, ?)",
        (question, answer, sources, datetime.datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()


def get_history(limit: int = 50) -> list[dict]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, question, answer, sources, created_at FROM qna_logs "
        "ORDER BY id DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]
