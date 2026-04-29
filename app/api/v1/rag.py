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
from app.core.logger import logger

router = APIRouter(prefix="/rag", tags=["RAG"])


# =========================
# RUN QUERY
# =========================
@router.post("/query")
@rate_limiter(limit=10, window=60)
async def query_rag(
    query: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await handle_query(
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
    search: str = None,
    language: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Query).filter(
        Query.user_id == current_user.id
    )

    #  search filter
    if search:
        query = query.filter(Query.question.ilike(f"%{search}%"))

    #  language filter
    if language:
        query = query.filter(Query.language == language)

    # sorting
    query = query.order_by(Query.created_at.desc())

    return paginate(query, page, limit)


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

    logger.info(f"Document uploaded: {filename} by admin {current_admin.id}")
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