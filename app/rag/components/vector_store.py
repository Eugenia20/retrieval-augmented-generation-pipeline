import faiss
import numpy as np

from app.rag.components.embeddings import embed_text

# in-memory store (upgrade later to persistent)
documents = []
index = None


# =========================
# BUILD INDEX (INITIAL LOAD)
# =========================
def build_index(texts: list[str]):
    global index, documents

    documents = texts.copy()

    embeddings = [embed_text(t) for t in texts]
    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)


# =========================
# ADD NEW DOCUMENTS
# =========================
def add_to_index(texts: list[str]):
    global index, documents

    if not texts:
        return

    embeddings = [embed_text(t) for t in texts]
    embeddings = np.array(embeddings).astype("float32")

    # If index doesn't exist → create it
    if index is None:
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)
    documents.extend(texts)


# =========================
# SEARCH
# =========================
def search(query: str, k: int = 3):
    global index, documents

    if index is None or len(documents) == 0:
        return []

    query_vector = embed_text(query)
    query_vector = np.array([query_vector]).astype("float32")

    distances, indices = index.search(query_vector, k)

    return [documents[i] for i in indices[0] if i < len(documents)]