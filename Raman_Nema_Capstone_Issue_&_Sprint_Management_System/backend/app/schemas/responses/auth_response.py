from pydantic import BaseModel

from datetime import datetime


class RegisterResponse(BaseModel):
    """User registration response schema."""

    message: str


class LoginResponse(BaseModel):
    """User login response schema."""

    access_token: str
    name: str
    role: str
    expires_at: datetime

class LogoutResponse(BaseModel):
    message: str