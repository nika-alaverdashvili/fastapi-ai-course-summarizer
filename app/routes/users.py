from fastapi import APIRouter, HTTPException, status, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.jwt import TokenResponse
from app.utils.security import decode_token

from sqlalchemy.future import select

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import hash_password
from app.utils.token import generate_tokens

router = APIRouter()


@router.post("/users", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Register a new user and return access + refresh tokens.
    """
    result = await db.execute(select(User).where(User.email == str(user.email)))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=user.name,
        email=str(user.email),
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return generate_tokens(user=new_user)


@router.post("/users/refresh", response_model=TokenResponse)
async def refresh_tokens(
    refresh_token: str = Body(..., embed=True),
    db: AsyncSession = Depends(get_db)
):
    """
    Verify the provided refresh token and return new access and refresh tokens.
    """
    payload = decode_token(refresh_token, expected_type="refresh")

    result = await db.execute(select(User).where(User.id == payload.uuid))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return generate_tokens(user=user)

