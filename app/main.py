from fastapi import FastAPI

from app.api.v1 import rag, auth, admin, users,admin_access,admin_stats
from app.db.session import engine
from app.rag.components.vector_store import load_index
from app.db.base_models import Base
import time
from fastapi import Request
from app.core.logger import logger

tags_metadata = [
    {
        "name": "Auth",
        "description": "Authentication operations (login, register, refresh, logout)"
    },
    {
        "name": "RAG",
        "description": "Query the AI system and manage documents"
    },
    {
        "name": "Admin",
        "description": "Admin operations (users, documents, analytics)"
    }
]
app = FastAPI(
    title="Enterprise LLM RAG Platform",
    description="""
🚀 Intelligent document-based AI system for enterprises.

### Features:
- 🔐 Secure authentication (JWT + refresh tokens)
- 📄 Document upload (PDF, DOCX, TXT)
- 🧠 RAG pipeline (retrieval + LLM)
- 🌍 Multilingual support (EN, RU, ZH)
- 📊 Admin analytics & monitoring

### Usage:
1. Login to get access token
2. Upload documents (admin only)
3. Query the system
4. View history & analytics
""",
    version="1.0.0",
    contact={
        "name": "Your Name",
        "email": "your@email.com"
    }
)

# =========================
# STARTUP
# =========================
@app.on_event("startup")
def startup_event():
    load_index()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = round(time.time() - start_time, 3)

    logger.info(
        f"{request.method} {request.url.path} "
        f"status={response.status_code} "
        f"time={duration}s"
    )

    return response
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
app.include_router(admin_access.router, prefix="/api/v1")

# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
def health():
    return {"status": "ok"}