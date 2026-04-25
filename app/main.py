from fastapi import FastAPI

from app.api.v1 import rag, auth, admin, users
from app.db.session import engine
from app.db.base import Base
from app.rag.components.vector_store import build_index
app = FastAPI(
    title="LLM RAG Platform",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():
    build_index([
        "Artificial Intelligence is the simulation of human intelligence.",
        "Machine learning is a subset of AI.",
        "Deep learning uses neural networks.",
        "AI is used in fraud detection systems.",
        "Natural language processing enables machines to understand text."
    ])
# Create tables (temporary, for development)
Base.metadata.create_all(bind=engine)

# =========================
# ROUTERS
# =========================

app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(rag.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")

# =========================
# HEALTH CHECK
# =========================

@app.get("/health")
def health():
    return {"status": "ok"}