from pydantic import BaseModel
from pydantic import EmailStr

from app.common.enums import Role


class RegisterRequest(BaseModel):
    """User registration request schema."""

    name: str
    email: EmailStr
    password: str
    role: Role


class LoginRequest(BaseModel):
    """User login request schema."""

    email: EmailStr
    password: str
