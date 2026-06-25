from pydantic import BaseModel


class RegisterResponse(BaseModel):
    """User registration response schema."""

    message: str
