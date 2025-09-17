from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import EmailStr

from app.api.deps import get_db
from app.db import models
from app.schemas.user import UserCreate, UserRead, Token
from app.core.security import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = models.User(email=payload.email, hashed_password=get_password_hash(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=Token)
async def login(request: Request, db: Session = Depends(get_db)):
    
    email: str | None = None
    password: str | None = None

    ct = (request.headers.get("content-type") or "").lower()

    if "application/x-www-form-urlencoded" in ct or "multipart/form-data" in ct:
        form = await request.form()
        email = (form.get("username") or form.get("email")) if form else None
        password = form.get("password") if form else None
    else:
        try:
            body = await request.json()
        except Exception:
            body = {}
        email = body.get("email") or body.get("username")
        password = body.get("password")

    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="email/username and password required",
        )

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email/username or password",
        )

    access_token = create_access_token(subject=user.email)
    return {"access_token": access_token, "token_type": "bearer"}
