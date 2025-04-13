from datetime import timedelta

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db
from app.models.user import User
from app.schemas.jwt import TokenResponse
from app.utils.security import create_token, decode_token

oauth2_scheme = HTTPBearer()


def generate_tokens(user) -> TokenResponse:
    """
    Generate access and refresh tokens for a user.
    """
    access_token = create_token(
        data={"sub": user.email, "uuid": str(user.id), "email": user.email},
        expires_delta=timedelta(minutes=2),
        token_type="access",
    )
    refresh_token = create_token(
        data={"sub": user.email, "uuid": str(user.id), "email": user.email},
        expires_delta=timedelta(minutes=15),
        token_type="refresh",
    )
    return TokenResponse.model_validate(
        {"access_token": access_token, "refresh_token": refresh_token}
    )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Decode and validate the access token and return the corresponding user.
    """
    token = credentials.credentials  # Extract token string
    payload = decode_token(token, expected_type="access")

    result = await db.execute(select(User).where(User.id == payload.uuid))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
