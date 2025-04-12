from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status
from jwt import PyJWTError
from passlib.context import CryptContext

from app.schemas.jwt import TokenPayload
from app.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify if the given password matches the hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def create_token(data: dict, expires_delta: timedelta, token_type: str) -> str:
    """Create a JWT token with given data and expiration."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire, "token_type": token_type})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str, expected_type: str) -> TokenPayload:
    """Decode and validate a JWT token. Raise error if invalid or expired."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenPayload(**payload)
    except (PyJWTError, ValueError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")

    if token_data.token_type != expected_type:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token type")

    return token_data
