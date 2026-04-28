from fastapi import APIRouter, Depends, Response, Request, HTTPException
from sqlalchemy.orm import Session
from jose import jwt
from app.db.session import get_db
from app.services.auth_service import create_user, authenticate_user
from app.core.security import create_access_token, create_refresh_token
from app.core.config import settings
from app.core.rate_limit import rate_limiter

router = APIRouter(prefix="/auth", tags=["Auth"])


# =========================
# REGISTER
# =========================

@router.post("/register")
def register(email: str, password: str, db: Session = Depends(get_db)):
    user = create_user(db, email, password)
    return {"message": "User created", "user_id": user.id}


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

    #  store refresh token in cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token_value,
        httponly=True,
        secure=False,   # change to True in production (HTTPS)
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
def refresh_access_token(request: Request):
    refresh_token_cookie = request.cookies.get("refresh_token")

    if not refresh_token_cookie:
        raise HTTPException(status_code=401, detail="Missing refresh token")

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
def logout(response: Response):
    response.delete_cookie("refresh_token")

    return {"message": "Logged out successfully"}