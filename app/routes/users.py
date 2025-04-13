from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db
from app.models.user import User
from app.schemas.jwt import TokenResponse
from app.schemas.user import PasswordChange, UserCreate, UserLogin, UserOut
from app.utils.security import decode_token, hash_password, verify_password
from app.utils.token import generate_tokens, get_current_user

router = APIRouter()


@router.post(
    "/users", response_model=TokenResponse, status_code=status.HTTP_201_CREATED
)
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
        hashed_password=hash_password(user.password),
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return generate_tokens(user=new_user)


@router.post("/users/refresh", response_model=TokenResponse)
async def refresh_tokens(
    refresh_token: str = Body(..., embed=True), db: AsyncSession = Depends(get_db)
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


@router.post("/users/login", response_model=TokenResponse)
async def login_user(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    """
    Authenticate a user via email and password, then return JWT tokens.
    """
    result = await db.execute(select(User).where(User.email == str(credentials.email)))
    user = result.scalar_one_or_none()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return generate_tokens(user=user)


@router.post("/users/change-password", status_code=200)
async def change_password(
    data: PasswordChange,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Allow an authenticated user to change their password.
    """
    if not verify_password(data.current_password, current_user.hashed_password):
        raise HTTPException(status_code=401, detail="Current password is incorrect")

    current_user.hashed_password = hash_password(data.new_password)
    db.add(current_user)
    await db.commit()

    return {"message": "Password changed successfully"}


@router.get("/users/me", response_model=UserOut)
async def get_user_details(current_user: User = Depends(get_current_user)):
    """
    Retrieve the details of the currently authenticated user.

    Returns the user's profile information.
    """
    return current_user
