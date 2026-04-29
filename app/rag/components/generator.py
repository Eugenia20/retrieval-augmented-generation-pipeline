import httpx
from app.core.config import settings


async def generate_answer(query: str, context: str, language: str):

    if not context.strip():
        return "I don't have enough information"

    prompt = f"""
You are an expert AI assistant.

Rules:
- Answer ONLY using the provided context
- If not found, say: "I don't have enough information"

Context:
{context}

Question:
{query}

Answer:
"""

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": settings.OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )

        return response.json().get("response", "").strip()

    except Exception:
        return "Error generating response"