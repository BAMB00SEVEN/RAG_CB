"""
Run this script whenever you add/change/remove files in data/docs/.

Usage:
    python scripts/build_index.py
"""
import sys
from pathlib import Path

# Allow running this script directly (adds project root to path)
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.config import DOCS_DIR, CHUNK_SIZE, CHUNK_OVERLAP
from app.utils.text_splitter import split_text
from app.rag.embeddings import embed_texts
from app.rag.vector_store import build_and_save_index


def main():
    if not DOCS_DIR.exists():
        print(f"Docs directory not found: {DOCS_DIR}")
        sys.exit(1)

    doc_files = sorted(DOCS_DIR.glob("*.txt"))
    if not doc_files:
        print(f"No .txt files found in {DOCS_DIR}. Add some documents first.")
        sys.exit(1)

    all_chunks = []
    metadata = []

    for doc_path in doc_files:
        text = doc_path.read_text(encoding="utf-8")
        chunks = split_text(text, CHUNK_SIZE, CHUNK_OVERLAP)
        for chunk in chunks:
            all_chunks.append(chunk)
            metadata.append({"text": chunk, "source": doc_path.name})

    print(f"Embedding {len(all_chunks)} chunks from {len(doc_files)} document(s)...")
    vectors = embed_texts(all_chunks)

    build_and_save_index(vectors, metadata)
    print(f"Index built: {len(all_chunks)} chunks from {len(doc_files)} documents")


if __name__ == "__main__":
    main()
