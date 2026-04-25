from app.rag.components.embeddings import embed_text
from app.rag.components.vector_store import add_to_index


def ingest_document(text: str):
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]

    embeddings = [embed_text(chunk) for chunk in chunks]

    add_to_index(chunks, embeddings)

    return {"message": "Document indexed successfully"}