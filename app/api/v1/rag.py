from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.rate_limit import rate_limiter
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.rag_service import handle_query
from app.services.ingestion_services import ingest_document
from app.models.query import Query
from app.utils.pagination import paginate

router = APIRouter(prefix="/rag", tags=["RAG"])

# RUN RAG QUERY (STORE + PROCESS)
@router.post("/query")
def query_rag(
    query: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(rate_limiter)
):
    return handle_query(db, current_user.id, query)

# GET USER HISTORY
@router.get("/history")
def get_history(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Query).filter(Query.user_id == current_user.id)

    return paginate(query, page, limit)

@router.post("/ingest")
def ingest(text: str):
    return ingest_document(text)