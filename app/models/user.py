from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.email == data.email).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user = User(
        email=data.email,
        phone=data.phone,
        password_hash=hash_password(data.password),
        is_active=False
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "status": "payment_required",
        "message": "Registration created. Please complete ₹10 payment.",
        "user_id": str(user.id),
        "email": user.email,
        "phone": user.phone
    }


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not user.password_hash or not verify_password(
        data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Please complete the ₹10 registration payment before login."
        )

    return {
        "access_token": create_access_token(str(user.id)),
        "token_type": "bearer"
    }
