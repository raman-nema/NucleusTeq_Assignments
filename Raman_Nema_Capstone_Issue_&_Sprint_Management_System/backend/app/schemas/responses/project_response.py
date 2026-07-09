from datetime import datetime

from pydantic import BaseModel
from app.common.pagination import PaginationMeta


class ProjectResponse(BaseModel):
    """Project response schema."""

    id: str
    name: str
    description: str
    created_by: str
    created_at: datetime
    updated_at: datetime


class ProjectListResponse(BaseModel):
    """Project list response schema."""

    projects: list[ProjectResponse]
    pagination: PaginationMeta


class DeleteProjectResponse(BaseModel):
    """Project deletion response schema."""

    message: str
