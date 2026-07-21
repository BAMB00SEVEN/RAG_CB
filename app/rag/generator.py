"""
Calls the Groq API to generate a final natural-language answer, grounded in
the retrieved context chunks.
"""
from groq import Groq
from app.config import GROQ_API_KEY, GROQ_MODEL

SYSTEM_PROMPT = (
    "You are a helpful, knowledgeable assistant. You may be given some retrieved "
    "context from a document knowledge base along with the user's question. "
    "If the context is relevant, use it and prioritize it (it may be more specific "
    "or up to date than what you already know). If the context is missing, empty, "
    "or not relevant to the question, simply answer using your own general knowledge "
    "instead - don't mention the context or say you lack information in that case. "
    "Be concise, clear, and accurate."
)

_client = None


def _get_client() -> Groq:
    global _client
    if _client is None:
        if not GROQ_API_KEY:
            raise RuntimeError(
                "GROQ_API_KEY is not set. Add it to your .env file (local) "
                "or Render Environment Variables (production)."
            )
        _client = Groq(api_key=GROQ_API_KEY)
    return _client


def generate_answer(question: str, context_chunks: list[str]) -> str:
    if context_chunks:
        context_text = "\n\n---\n\n".join(context_chunks)
        user_prompt = (
            f"Retrieved context (may or may not be relevant):\n{context_text}\n\n"
            f"Question: {question}\n\n"
            "If the context above helps answer the question, use it. Otherwise, "
            "just answer normally using your own knowledge."
        )
    else:
        user_prompt = question

    client = _get_client()
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=512,
    )
    return response.choices[0].message.content.strip()
