import faiss
import numpy as np
import os
import json

from app.rag.components.embeddings import embed_text


FAISS_PATH = "faiss.index"
DOCS_PATH = "documents.json"

# =========================
# GLOBAL STORE
# =========================
documents = []
index = None


# =========================
# ADD TO INDEX (APPEND)
# =========================
def add_to_index(items: list[dict]):
    global index, documents

    texts = [item["text"] for item in items]

    embeddings = [embed_text(t) for t in texts]
    embeddings = np.array(embeddings).astype("float32")

    if index is None:
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)
    documents.extend([
        {
            "text": item["text"],
            "document_id": item["document_id"],
            "department": item.get("department"),
            "embedding": emb.tolist()
        }
        for item, emb in zip(items, embeddings)
    ])

    #  SAVE AFTER ADDING
    save_index()


# =========================
# SEARCH
# =========================
def search(query: str, k: int = 3):
    global index, documents

    if index is None:
        return []

    query_vector = np.array(embed_text(query)).astype("float32")
    query_vector = np.array([query_vector]).astype("float32")

    distances, indices = index.search(query_vector, k)

    results = []
    for i in indices[0]:
        if i < len(documents):  # safety check
            results.append(documents[i])

    return results


# =========================
# SAVE INDEX
# =========================
def save_index():
    if index is not None:
        faiss.write_index(index, FAISS_PATH)

        with open(DOCS_PATH, "w", encoding="utf-8") as f:
            json.dump(documents, f, ensure_ascii=False)


# =========================
# LOAD INDEX
# =========================
def load_index():
    global index, documents

    if os.path.exists(FAISS_PATH):
        index = faiss.read_index(FAISS_PATH)

    if os.path.exists(DOCS_PATH):
        with open(DOCS_PATH, "r", encoding="utf-8") as f:
            documents = json.load(f)