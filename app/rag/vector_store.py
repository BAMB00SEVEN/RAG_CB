"""
Handles building, saving, loading, and searching the FAISS vector index.
"""
import json
import faiss
import numpy as np
from app.config import INDEX_DIR, INDEX_FILE, METADATA_FILE


def build_and_save_index(vectors: np.ndarray, metadata: list[dict]) -> None:
    """metadata[i] must correspond to vectors[i], e.g. {"text": ..., "source": ...}"""
    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(vectors)

    faiss.write_index(index, str(INDEX_FILE))
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False)


def load_index():
    if not INDEX_FILE.exists() or not METADATA_FILE.exists():
        raise FileNotFoundError(
            "FAISS index not found. Run `python scripts/build_index.py` first."
        )
    index = faiss.read_index(str(INDEX_FILE))
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return index, metadata


def search(index, metadata: list[dict], query_vector: np.ndarray, top_k: int) -> list[dict]:
    query_vector = np.array([query_vector]).astype("float32")
    distances, indices = index.search(query_vector, top_k)

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx == -1:
            continue
        item = dict(metadata[idx])
        item["distance"] = float(dist)
        results.append(item)
    return results
