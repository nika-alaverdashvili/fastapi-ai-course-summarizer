from uuid import uuid4
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.utils.security import hash_password

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)) -> UserOut:
    """
    Register a new user.

    This endpoint creates a new user account with a unique email address.
    The user's password is securely hashed before being stored in the database.

    Returns:
        UserOut: The newly created user's public information.
    """
    existing_user = await db.scalar(select(User).where(User.email == str(user.email)))
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already registered")

    hashed_pw = hash_password(user.password)

    new_user = User(
        id=uuid4(),
        name=user.name,
        email=str(user.email),
        hashed_password=hashed_pw,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return UserOut.model_validate(new_user)

