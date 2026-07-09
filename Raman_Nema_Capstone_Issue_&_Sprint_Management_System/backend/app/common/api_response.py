from typing import Any
from pydantic import BaseModel


class ApiResponse(BaseModel):
    """Consistent response envelope used across API endpoints."""

    success: bool
    message: str
    data: Any | None = None
