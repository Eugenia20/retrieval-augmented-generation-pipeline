from app.rag.components.vector_store import add_to_index
import re

# =========================
# TEXT CHUNKING
# =========================
def chunk_text(text: str, max_size: int = 500):
    sentences = re.split(r'(?<=[.!?]) +', text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_size:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

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