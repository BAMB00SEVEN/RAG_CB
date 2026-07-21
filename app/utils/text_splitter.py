"""
Splits long text into smaller overlapping chunks so each chunk fits nicely
into an embedding and gives the LLM a focused piece of context.
"""


def split_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    text = " ".join(text.split())  # normalize whitespace
    if not text:
        return []

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
        start = end - chunk_overlap  # step forward, keeping some overlap
    return chunks
