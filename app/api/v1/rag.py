from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.core.rate_limit import rate_limiter
from app.db.session import get_db
from app.core.dependencies import get_current_user, get_current_admin

from app.models.user import User
from app.models.query import Query
from app.models.document import Document

from app.services.rag_service import handle_query
from app.services.ingestion_services import ingest_document
from app.services.file_parser import parse_pdf, parse_docx, parse_txt

from app.utils.pagination import paginate


router = APIRouter(prefix="/rag", tags=["RAG"])


# =========================
# RUN QUERY
# =========================
@router.post("/query")
@rate_limiter(limit=10, window=60)
def query_rag(
    query: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return handle_query(
        db,
        current_user.id,
        current_user.employee_id,
        current_user.department,
        query
    )


# =========================
# USER HISTORY
# =========================
@router.get("/history")
def get_history(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_queries = db.query(Query).filter(
        Query.user_id == current_user.id
    )

    return paginate(user_queries, page, limit)


# =========================
# FILE UPLOAD (ADMIN)
# =========================
@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    filename = file.filename.lower()

    # =========================
    # PARSE FILE
    # =========================
    if filename.endswith(".pdf"):
        text = parse_pdf(file)

    elif filename.endswith(".docx"):
        text = parse_docx(file)

    elif filename.endswith(".txt"):
        text = parse_txt(file)

    else:
        return {"error": "Unsupported file type"}

    # =========================
    # SAVE DOCUMENT METADATA
    # =========================
    doc = Document(
        filename=filename,
        department=current_admin.department,
        uploaded_by=current_admin.id
    )

    db.add(doc)
    db.commit()
    db.refresh(doc)

    # =========================
    # INGEST
    # =========================
    return ingest_document(
        text,
        document_id=doc.id,
        department=current_admin.department
    )