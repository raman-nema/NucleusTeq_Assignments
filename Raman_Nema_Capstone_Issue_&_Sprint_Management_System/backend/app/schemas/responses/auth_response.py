from pydantic import BaseModel

from datetime import datetime


class RegisterResponse(BaseModel):
    """User registration response schema."""

    message: str


class LoginResponse(BaseModel):
    """User login response schema."""

    access_token: str
    role: str
    expires_at: datetime
