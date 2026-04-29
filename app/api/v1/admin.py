from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.query import Query
from app.models.evaluation import Evaluation
from app.models.document import Document

from app.core.dependencies import get_current_admin
from app.utils.pagination import paginate

router = APIRouter(prefix="/admin", tags=["Admin"])


# =========================
# USERS (PAGINATED)
# =========================
@router.get("/users")
def get_users(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    query = db.query(User).order_by(User.created_at.desc())
    return paginate(query, page, limit)


# =========================
# ACTIVATE / DEACTIVATE (MERGED)
# =========================
@router.patch("/users/{user_id}/status")
def update_user_status(
    user_id: int,
    is_active: bool,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = is_active
    db.commit()

    return {
        "message": f"User {'activated' if is_active else 'deactivated'}"
    }


# =========================
# QUERIES (PAGINATED)
# =========================
@router.get("/queries")
def get_all_queries(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    query = db.query(Query).order_by(Query.created_at.desc())
    return paginate(query, page, limit)


# =========================
# DOCUMENTS (IMPORTANT FOR RAG)
# =========================
@router.get("/documents")
def get_documents(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    query = db.query(Document).order_by(Document.created_at.desc())
    return paginate(query, page, limit)


# =========================
# EVALUATIONS (FIXED PAGINATION)
# =========================
@router.get("/evaluations")
def get_evaluations(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    query = db.query(Evaluation).order_by(Evaluation.created_at.desc())
    return paginate(query, page, limit)