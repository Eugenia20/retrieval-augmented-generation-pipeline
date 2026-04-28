from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.core.security import hash_password, verify_password
from app.core.config import settings
import re


# DOMAIN VALIDATION
def validate_email_domain(email: str):
    domain = email.split("@")[-1]

    if domain not in settings.ALLOWED_DOMAINS:
        raise HTTPException(status_code=400, detail="Invalid email domain")


# CREATE USER
def create_user(
    db: Session,
    email: str,
    password: str,
    department: str,
    is_admin: bool = False
):
    validate_email_domain(email)
    validate_password(password)

    # normalize department
    department = department.strip().lower()

    # generate employee ID
    prefix = get_prefix(department)
    employee_id = generate_employee_id(db, prefix)

    user = User(
        email=email,
        password_hash=hash_password(password),
        is_admin=is_admin,
        employee_id=employee_id,
        department=department
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "User created",
        "user_id": user.id,
        "employee_id": user.employee_id,
        "department": user.department
    }

def generate_employee_id(db: Session, prefix: str):
    last_user = (
        db.query(User)
        .filter(User.employee_id.like(f"{prefix}%"))
        .order_by(User.employee_id.desc())
        .first()
    )

    if not last_user:
        return f"{prefix}0001"

    last_number = int(last_user.employee_id[len(prefix):])
    return f"{prefix}{last_number + 1:04d}"

def get_prefix(department: str):
    mapping = {
        "Tech": "T2",
        "Business": "B2",
        "Hr": "H2",
        "Admin": "A2"
    }
    return mapping.get(department.lower(), "U2")

def validate_password(password: str):
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")

    if not re.search(r"[A-Z]", password):
        raise HTTPException(status_code=400, detail="Password must contain an uppercase letter")

    if not re.search(r"[0-9]", password):
        raise HTTPException(status_code=400, detail="Password must contain a number")

    if not re.search(r"[!@#$%^&*()_+=\-]", password):
        raise HTTPException(status_code=400, detail="Password must contain a special character")

# AUTHENTICATE USER


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is deactivated")

    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return user

