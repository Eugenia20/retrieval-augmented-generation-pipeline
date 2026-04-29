import numpy as np
from app.rag.components.embeddings import embed_text


def rerank(query: str, docs: list[dict], top_k: int = 3):

    query_vec = np.array(embed_text(query))
    query_norm = query_vec / np.linalg.norm(query_vec)

    rescored = []

    for d in docs:
        doc_vec = np.array(d["embedding"])
        doc_norm = doc_vec / np.linalg.norm(doc_vec)

        score = np.dot(query_norm, doc_norm)

        rescored.append({**d, "score": score})

    rescored.sort(key=lambda x: x["score"], reverse=True)

    return rescored[:top_k]