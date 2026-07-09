from datetime import datetime

from pydantic import BaseModel


class AdminTotalsResponse(BaseModel):
    """Admin dashboard totals response schema."""

    projects: int
    sprints: int
    issues: int
    users: int


class AdminUserResponse(BaseModel):
    """Admin user row response schema."""

    id: str
    name: str
    email: str
    role: str
    created_at: datetime | None = None
    updated_at: datetime | None = None


class AdminDashboardResponse(BaseModel):
    """Admin dashboard response schema."""

    totals: AdminTotalsResponse
    users: list[AdminUserResponse]


class AdminUserListResponse(BaseModel):
    """Admin user list response schema."""

    users: list[AdminUserResponse]
