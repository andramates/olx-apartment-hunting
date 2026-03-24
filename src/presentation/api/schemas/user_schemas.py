from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    created_at: datetime | None = None