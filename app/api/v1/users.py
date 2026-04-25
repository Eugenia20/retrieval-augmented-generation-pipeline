from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/profile", tags=["User"])



# GET PROFILE


@router.get("/")
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "is_admin": current_user.is_admin
    }



# UPDATE PROFILE


@router.put("/")
def update_profile(
    new_email: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    current_user.email = new_email
    db.commit()
    db.refresh(current_user)

    return {"message": "Profile updated"}