from fastapi import APIRouter, Depends, Response, Request, HTTPException
from sqlalchemy.orm import Session
from jose import jwt
from app.db.session import get_db
from app.services.auth_service import create_user, authenticate_user
from app.core.security import create_access_token, create_refresh_token
from app.core.config import settings
from app.core.rate_limit import rate_limiter
from app.models.refresh_token import RefreshToken

router = APIRouter(prefix="/auth", tags=["Auth"])


# =========================
# REGISTER
# =========================

@router.post("/register")
def register(
    email: str,
    password: str,
    department: str,
    db: Session = Depends(get_db)
):
    return create_user(db, email, password, department)



# =========================
# LOGIN
# =========================

@router.post("/login")
@rate_limiter(limit=5, window=60)
def login(
    request: Request,
    email: str,
    password: str,
    response: Response,
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, email, password)

    access_token = create_access_token({
        "sub": str(user.id),
        "is_admin": user.is_admin
    })

    refresh_token_value = create_refresh_token({
        "sub": str(user.id)
    })

    #  SAVES IN DB
    db.add(RefreshToken(
        user_id=user.id,
        token=refresh_token_value
    ))
    db.commit()

    #  COOKIE
    response.set_cookie(
        key="refresh_token",
        value=refresh_token_value,
        httponly=True,
        secure=False,
        samesite="lax"
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# =========================
# REFRESH TOKEN
# =========================

@router.post("/refresh")
def refresh_access_token(
    request: Request,
    db: Session = Depends(get_db)
):
    refresh_token_cookie = request.cookies.get("refresh_token")

    if not refresh_token_cookie:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    #  CHECKs DB FIRST
    token_in_db = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token_cookie,
        RefreshToken.is_revoked == False
    ).first()

    if not token_in_db:
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        payload = jwt.decode(
            refresh_token_cookie,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id = payload.get("sub")

        new_access_token = create_access_token({
            "sub": user_id
        })

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
# =========================
# LOGOUT
# =========================

@router.post("/logout")
def logout(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    refresh_token = request.cookies.get("refresh_token")

    if refresh_token:
        db.query(RefreshToken).filter(
            RefreshToken.token == refresh_token
        ).update({"is_revoked": True})

        db.commit()

    response.delete_cookie("refresh_token")

    return {"message": "Logged out successfully"}