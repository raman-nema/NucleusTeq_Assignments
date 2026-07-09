from datetime import datetime
from pydantic import BaseModel
from app.common.pagination import PaginationMeta


class ProjectMemberSummary(BaseModel):
    """Basic member details shown on project cards."""

    id: str
    name: str
    role: str


class ProjectResponse(BaseModel):
    """Project response schema."""

    id: str
    name: str
    description: str
    created_by: str
    members: list[ProjectMemberSummary]
    created_at: datetime
    updated_at: datetime

class ProjectListResponse(BaseModel):
    """Project list response schema."""

    projects: list[ProjectResponse]
    pagination: PaginationMeta | None = None


class DeleteProjectResponse(BaseModel):
    """Project deletion response schema."""

    message: str


class ProjectMemberResponse(BaseModel):
    """Project member action response schema."""

    message: str
