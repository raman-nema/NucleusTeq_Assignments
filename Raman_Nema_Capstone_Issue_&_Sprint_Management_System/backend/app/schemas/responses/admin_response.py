from pydantic import BaseModel


class AdminDashboardResponse(BaseModel):
    """Admin dashboard user summary response schema."""

    name: str
    email: str
    role: str
