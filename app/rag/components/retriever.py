import numpy as np
from app.rag.components.vector_store import search
from app.rag.components.embeddings import embed_text


def retrieve_documents(query: str, language: str, k: int = 5):
    # =========================
    # 1. Get initial candidates
    # =========================
    candidates = search(query, k=10)  # get more first

    if not candidates:
        return []

    # =========================
    # 2. Embed query
    # =========================
    query_vec = np.array(embed_text(query))

    # =========================
    # 3. Score each document
    # =========================
    scored_docs = []

    for doc in candidates:
        doc_vec = np.array(embed_text(doc))

        # cosine similarity
        score = np.dot(query_vec, doc_vec) / (
            np.linalg.norm(query_vec) * np.linalg.norm(doc_vec)
        )
        if score > 0.3:
            scored_docs.append((doc, score))
        scored_docs.append((doc, score))

    # =========================
    # 4. Sort by relevance
    # =========================
    scored_docs.sort(key=lambda x: x[1], reverse=True)

    # =========================
    # 5. Return top-k
    # =========================
    return [doc for doc, _ in scored_docs[:k]]