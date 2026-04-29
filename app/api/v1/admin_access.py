from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import get_current_admin
from app.models.document_access import DocumentAccess
from app.models.document import Document

router = APIRouter(prefix="/admin/access", tags=["Admin Access"])

@router.get("/")
def get_all_access(
    db: Session = Depends(get_db),
    _=Depends(get_current_admin)
):
    logs = db.query(DocumentAccess).all()

    return [
        {
            "user_id": l.user_id,
            "document_id": l.document_id,
            "query_id": l.query_id,
            "timestamp": l.accessed_at
        }
        for l in logs
    ]
from sqlalchemy import func

@router.get("/documents")
def document_usage(
    db: Session = Depends(get_db),
    _=Depends(get_current_admin)
):
    results = (
        db.query(
            DocumentAccess.document_id,
            func.count(DocumentAccess.id).label("usage_count")
        )
        .group_by(DocumentAccess.document_id)
        .order_by(func.count(DocumentAccess.id).desc())
        .all()
    )

    docs = db.query(Document).all()
    doc_map = {d.id: d.filename for d in docs}

    return [
        {
            "document_id": r.document_id,
            "filename": doc_map.get(r.document_id, "unknown"),
            "usage_count": r.usage_count
        }
        for r in results
    ]
@router.get("/users")
def user_activity(
    db: Session = Depends(get_db),
    _=Depends(get_current_admin)
):
    results = (
        db.query(
            DocumentAccess.user_id,
            func.count(DocumentAccess.id).label("count")
        )
        .group_by(DocumentAccess.user_id)
        .order_by(func.count(DocumentAccess.id).desc())
        .all()
    )

    return [
        {
            "user_id": r.user_id,
            "documents_accessed": r.count
        }
        for r in results
    ]