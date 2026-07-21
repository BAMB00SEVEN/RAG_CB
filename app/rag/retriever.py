"""
Given a user question, finds the most relevant document chunks.
"""
from functools import lru_cache
from app.config import TOP_K
from app.rag.embeddings import embed_query
from app.rag import vector_store


@lru_cache(maxsize=1)
def _load_index_cached():
    return vector_store.load_index()


def retrieve(question: str, top_k: int = TOP_K) -> list[dict]:
    index, metadata = _load_index_cached()
    query_vector = embed_query(question)
    return vector_store.search(index, metadata, query_vector, top_k)
