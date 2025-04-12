from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class TokenPayload(BaseModel):
    sub: str
    uuid: UUID
    email: EmailStr
    exp: datetime
    token_type: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    