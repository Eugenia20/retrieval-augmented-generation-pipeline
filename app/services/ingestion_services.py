from app.rag.components.vector_store import add_to_index


# =========================
# TEXT CHUNKING
# =========================
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


# =========================
# INGEST DOCUMENT
# =========================
def ingest_document(text: str, document_id: int, department: str):
    chunks = chunk_text(text)

    chunks_with_meta = [
        {
            "text": chunk,
            "document_id": document_id,
            "department": department   #
        }
        for chunk in chunks
    ]

    add_to_index(chunks_with_meta)

    return {
        "message": "Document indexed successfully",
        "chunks": len(chunks)
    }