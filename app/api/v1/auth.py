from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.rate_limit import rate_limiter
from app.db.session import get_db
from app.services.auth_service import create_user, authenticate_user
from app.core.security import create_access_token, create_refresh_token
from fastapi import Response
router = APIRouter(prefix="/auth", tags=["Auth"])
from fastapi import Request

@router.post("/register")
def register(email: str, password: str, db: Session = Depends(get_db)):
    user = create_user(db, email, password)

    return {"message": "User created", "user_id": user.id}


@router.post("/login")
def login(
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

    refresh_token = create_refresh_token({
        "sub": str(user.id)
    })

    #  STORES REFRESH TOKEN IN COOKIE
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,     #  cannot be accessed by JS
        secure=False,      #  (HTTPS)
        samesite="lax"
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/refresh")
def refresh_token(request: Request):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    try:
        payload = jwt.decode(
            refresh_token,
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