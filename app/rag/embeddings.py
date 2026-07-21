"""
Wraps a local, lightweight embedding model (via fastembed, which uses ONNX
runtime instead of PyTorch) that turns text into vectors. Runs fully
offline/locally - no API key needed for this part. Chosen specifically to
keep memory usage low enough for free hosting tiers (e.g. Render's 512MB).
"""
from functools import lru_cache
import numpy as np
from fastembed import TextEmbedding
from app.config import EMBEDDING_MODEL


@lru_cache(maxsize=1)
def get_embedder() -> TextEmbedding:
    return TextEmbedding(model_name=EMBEDDING_MODEL)


def embed_texts(texts: list[str]) -> np.ndarray:
    model = get_embedder()
    vectors = list(model.embed(texts))
    return np.array(vectors, dtype="float32")


def embed_query(text: str) -> np.ndarray:
    return embed_texts([text])[0]
