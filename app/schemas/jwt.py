from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


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
