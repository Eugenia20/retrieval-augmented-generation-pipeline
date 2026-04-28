import numpy as np
from app.rag.components.vector_store import search
from app.rag.components.embeddings import embed_text


def retrieve_documents(
    query: str,
    language: str,
    user_department: str,
    k: int = 5
):
    # =========================
    # 1. Get candidates
    # =========================
    candidates = search(query, k=10)

    if not candidates:
        return []

    # =========================
    # 2. Embed query
    # =========================
    query_vec = np.array(embed_text(query))

    scored_docs = []

    # =========================
    # 3. Score each document
    # =========================
    for item in candidates:

        # 🔐 SECURITY FILTER
        if item.get("department") != user_department:
            continue

        text = item["text"]

        #  USE STORED EMBEDDING
        doc_vec = np.array(item["embedding"])

        score = np.dot(query_vec, doc_vec) / (
            np.linalg.norm(query_vec) * np.linalg.norm(doc_vec)
        )

        if score > 0.3:
            scored_docs.append({
                "text": text,
                "document_id": item["document_id"],
                "department": item.get("department"),
                "score": score
            })

    # =========================
    # 4. Sort
    # =========================
    scored_docs.sort(key=lambda x: x["score"], reverse=True)

    # =========================
    # 5. Return top-k
    # =========================
    return scored_docs[:k]