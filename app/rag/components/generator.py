import requests
from app.core.config import settings


def generate_answer(query: str, context: str, language: str):
    # =========================
    # 1. Handle empty context
    # =========================
    if not context or not context.strip():
        return "I don't have enough information"

    # =========================
    # 2. Strong prompt
    # =========================
    prompt = f"""
You are an expert AI assistant.

Rules:
- Answer ONLY using the provided context
- Do NOT make up information
- If the answer is not in the context, say:
  "I don't have enough information"
- Be clear, structured, and concise
- Use bullet points if helpful
- Answer in the same language as the question

Context:
{context}

Question:
{query}

Answer:
"""

    # =========================
    # 3. Call Ollama safely
    # =========================
    try:
        response = requests.post(
            f"{settings.OLLAMA_BASE_URL}/api/generate",
            json={
                "model": settings.OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2,   #  less randomness
                    "num_predict": 200    # control response length
                }
            },
            timeout=30
        )

        return response.json().get("response", "").strip()

    except Exception as e:
        print(f"[LLM ERROR]: {e}")
        return "Error generating response"