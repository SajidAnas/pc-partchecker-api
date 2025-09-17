from datetime import datetime, timedelta, timezone
from typing import Any, Optional
import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password: str) -> str: return pwd_context.hash(password)
def verify_password(plain: str, hashed: str) -> bool: return pwd_context.verify(plain, hashed)

def create_access_token(subject: str, expires_minutes: Optional[int] = None) -> str:
    exp = datetime.now(tz=timezone.utc) + timedelta(minutes=expires_minutes or settings.access_token_expire_minutes)
    return jwt.encode({"sub": subject, "exp": exp}, settings.secret_key, algorithm=settings.algorithm)

def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
