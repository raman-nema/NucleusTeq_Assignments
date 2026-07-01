from datetime import datetime
from pydantic import BaseModel

class ProjectResponse(BaseModel):
    """Project response schema."""

    id: str
    name: str
    description: str
    created_by: str
    members: list[str]
    created_at: datetime
    updated_at: datetime

class ProjectListResponse(BaseModel):
    """Project list response schema."""

    projects: list[ProjectResponse]

class DeleteProjectResponse(BaseModel):
    """Project deletion response schema."""

    message: str

class ProjectMemberResponse(BaseModel):
    """Project member operation response."""

    message: str