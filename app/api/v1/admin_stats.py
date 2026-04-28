from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.session import get_db
from app.core.dependencies import get_current_admin
from app.models.user import User
from app.models.query import Query
from app.models.document import Document
from app.models.evaluation import Evaluation

router = APIRouter(prefix="/admin/stats", tags=["Admin Stats"])

@router.get("/overview")
def system_overview(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    return {
        "total_users": db.query(User).count(),
        "total_queries": db.query(Query).count(),
        "total_documents": db.query(Document).count()
    }
@router.get("/top-users")
def top_users(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    results = (
        db.query(Query.user_id, func.count(Query.id).label("count"))
        .group_by(Query.user_id)
        .order_by(func.count(Query.id).desc())
        .limit(5)
        .all()
    )

    return [
        {"user_id": r.user_id, "queries": r.count}
        for r in results
    ]
import json

@router.get("/top-documents")
def top_documents(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    queries = db.query(Query).all()

    usage = {}

    for q in queries:
        if not q.retrieved_docs:
            continue

        docs = json.loads(q.retrieved_docs)

        for d in docs:
            doc_id = d["document_id"]
            usage[doc_id] = usage.get(doc_id, 0) + 1

    sorted_docs = sorted(usage.items(), key=lambda x: x[1], reverse=True)[:5]

    docs = db.query(Document).filter(
        Document.id.in_([d[0] for d in sorted_docs])
    ).all()

    doc_map = {d.id: d.filename for d in docs}

    return [
        {
            "document_id": doc_id,
            "filename": doc_map.get(doc_id, "unknown"),
            "usage_count": count
        }
        for doc_id, count in sorted_docs
    ]
@router.get("/hallucination-rate")
def hallucination_rate(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    total = db.query(Evaluation).count()

    if total == 0:
        return {"rate": 0}

    flagged = db.query(Evaluation).filter(
        Evaluation.hallucination_flag == True
    ).count()

    return {"rate": flagged / total}

@router.get("/confidence")
def avg_confidence(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    avg = db.query(func.avg(Evaluation.confidence_score)).scalar()

    return {"average_confidence": avg or 0}

