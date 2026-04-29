import numpy as np
from app.rag.components.vector_store import search
from app.rag.components.embeddings import embed_text
from app.rag.components.bm25_store import search_bm25


def retrieve_documents(query: str, language: str, user_department: str, k: int = 5):

    # =========================
    # 1. Get FAISS + BM25
    # =========================
    faiss_results = search(query, k=10)
    bm25_results = search_bm25(query, faiss_results, k=10)

    # =========================
    # 2. Merge (remove duplicates)
    # =========================
    combined = {id(item): item for item in faiss_results}

    for item in bm25_results:
        combined[id(item)] = item

    candidates = list(combined.values())

    if not candidates:
        return []

    # =========================
    # 3. Embed query
    # =========================
    query_vec = np.array(embed_text(query))
    query_norm = query_vec / np.linalg.norm(query_vec)

    scored_docs = []

    # =========================
    # 4. Score + filter
    # =========================
    for item in candidates:

        # 🔐 department filter
        if item.get("department") != user_department:
            continue

        doc_vec = np.array(item["embedding"])
        doc_norm = doc_vec / np.linalg.norm(doc_vec)

        score = np.dot(query_norm, doc_norm)

        if score > 0.3:
            scored_docs.append({
                "text": item["text"],
                "document_id": item["document_id"],
                "department": item.get("department"),
                "embedding": item["embedding"],
                "score": score
            })

    # =========================
    # 5. Sort
    # =========================
    scored_docs.sort(key=lambda x: x["score"], reverse=True)

    return scored_docs[:k]