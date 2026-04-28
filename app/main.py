from fastapi import FastAPI

from app.api.v1 import rag, auth, admin, users
from app.db.session import engine
from app.db.base import Base
from app.rag.components.vector_store import load_index
from app.api.v1 import admin_stats



app = FastAPI(
    title="LLM RAG Platform",
    version="1.0.0"
)

# =========================
# STARTUP
# =========================
@app.on_event("startup")
def startup_event():
    load_index()


# =========================
# CREATE TABLES (DEV ONLY)
# =========================
Base.metadata.create_all(bind=engine)


# =========================
# ROUTERS
# =========================
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(rag.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
app.include_router(admin_stats.router, prefix="/api/v1")

# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
def health():
    return {"status": "ok"}