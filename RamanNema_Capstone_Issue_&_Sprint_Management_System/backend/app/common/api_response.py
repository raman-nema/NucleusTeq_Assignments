from typing import Any
from pydantic import BaseModel


class ApiResponse(BaseModel):
    """Consistent response envelope used across API endpoints."""

    # True when the operation completed as expected.
    success: bool

    # Client-facing summary of the outcome.
    message: str

    # Endpoint-specific response body, when there is data to return.
    data: Any | None = None
