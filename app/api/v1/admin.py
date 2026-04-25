from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.models.evaluation import Evaluation
from app.core.dependencies import get_current_admin
from app.models.query import Query
from app.utils.pagination import paginate

router = APIRouter(prefix="/admin", tags=["Admin"])

# =========================
# GET ALL USERS
# =========================

@router.get("/users")
def get_users(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    users = db.query(User).offset(offset).limit(limit).all()

    return [
        {
            "id": u.id,
            "email": u.email,
            "is_active": u.is_active,
            "is_admin": u.is_admin
        }
        for u in users
    ]


# =========================
# ACTIVATE USER
# =========================

@router.patch("/users/{user_id}/activate")
def activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = True
    db.commit()

    return {"message": "User activated"}


# =========================
# DEACTIVATE USER
# =========================

@router.patch("/users/{user_id}/deactivate")
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = False
    db.commit()

    return {"message": "User deactivated"}


# =========================
# GET ALL QUERIES (ADMIN VIEW)
# =========================

@router.get("/queries")
def get_all_queries(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    query = db.query(Query)

    return paginate(query, page, limit)


# =========================
# GET ALL EVALUATIONS
# =========================

@router.get("/evaluations")
def get_evaluations(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    evaluations = db.query(Evaluation).offset(offset).limit(limit).all()

    return evaluations