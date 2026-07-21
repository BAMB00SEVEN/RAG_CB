"""
Wraps a local sentence-transformers model that turns text into vectors.
Runs fully offline/locally - no API key needed for this part.
"""
from functools import lru_cache
import numpy as np
from sentence_transformers import SentenceTransformer
from app.config import EMBEDDING_MODEL


@lru_cache(maxsize=1)
def get_embedder() -> SentenceTransformer:
    # Cached so the (fairly large) model is only loaded into memory once.
    return SentenceTransformer(EMBEDDING_MODEL)


def embed_texts(texts: list[str]) -> np.ndarray:
    model = get_embedder()
    vectors = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    return vectors.astype("float32")


def embed_query(text: str) -> np.ndarray:
    return embed_texts([text])[0]
