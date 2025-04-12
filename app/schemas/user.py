from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=6)

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "password": "secure password"
            }
        }
    }


class UserOut(BaseModel):
    id: UUID
    name: str
    email: EmailStr

    model_config = {
        "from_attributes": True
    }
