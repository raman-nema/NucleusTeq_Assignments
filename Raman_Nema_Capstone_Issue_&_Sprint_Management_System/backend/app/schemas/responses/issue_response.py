from datetime import datetime

from pydantic import BaseModel


class IssueResponse(BaseModel):
    """Issue response schema."""

    id: str
    project_id: str
    sprint_id: str | None = None
    title: str
    description: str
    priority: str
    status: str
    assignee: str
    reporter: str
    created_at: datetime
    updated_at: datetime


class IssueListResponse(BaseModel):
    """Issue list response schema."""

    issues: list[IssueResponse]


class DeleteIssueResponse(BaseModel):
    """Issue deletion response schema."""

    message: str
