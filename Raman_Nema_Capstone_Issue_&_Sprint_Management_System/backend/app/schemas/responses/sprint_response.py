from datetime import datetime, date
from pydantic import BaseModel


class SprintResponse(BaseModel):
    """Sprint response schema."""

    id: str
    project_id: str
    name: str
    goal: str
    start_date: date
    end_date: date
    status: str
    created_by: str
    created_at: datetime
    updated_at: datetime


class SprintListResponse(BaseModel):
    """Sprint list response schema."""

    sprints: list[SprintResponse]


class DeleteSprintResponse(BaseModel):
    """Sprint deletion response schema."""

    message: str
