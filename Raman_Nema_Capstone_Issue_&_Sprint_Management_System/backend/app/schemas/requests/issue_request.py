from typing import Literal

from pydantic import (
    BaseModel,
    Field,
)


class IssueRequest(BaseModel):
    """Base issue request schema."""

    title: str = Field(
        min_length=3,
        max_length=100,
    )

    description: str = Field(
        min_length=10,
        max_length=500,
    )

    assignee: str

    sprint_id: str

    priority: Literal[
        "LOW",
        "MEDIUM",
        "HIGH",
    ] = "MEDIUM"

    type: Literal[
        "TASK",
        "BUG",
        "STORY",
    ] = "TASK"

    status: Literal[
        "TODO",
        "IN_PROGRESS",
        "DONE",
    ] = "TODO"


class CreateIssueRequest(IssueRequest):
    """Issue creation request schema."""


class UpdateIssueRequest(IssueRequest):
    """Issue update request schema."""
