"""
Calls the Groq API to generate a final natural-language answer, grounded in
the retrieved context chunks.
"""
from groq import Groq
from app.config import GROQ_API_KEY, GROQ_MODEL

SYSTEM_PROMPT = (
    "You are a helpful assistant that answers questions using ONLY the provided "
    "context. If the answer is not contained in the context, say you don't have "
    "enough information in the knowledge base to answer that. Be concise and clear."
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
    context_text = "\n\n---\n\n".join(context_chunks) if context_chunks else "No context found."

    user_prompt = (
        f"Context:\n{context_text}\n\n"
        f"Question: {question}\n\n"
        "Answer the question using only the context above."
    )

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
