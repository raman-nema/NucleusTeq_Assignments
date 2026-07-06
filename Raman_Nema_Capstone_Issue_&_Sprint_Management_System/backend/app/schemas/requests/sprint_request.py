from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class SprintRequest(BaseModel):
    """Base sprint request schema."""

    name: str = Field(
        min_length=3,
        max_length=100,
    )

    goal: str = Field(
        min_length=10,
        max_length=500,
    )

    start_date: date

    end_date: date

    status: Literal["PLANNED", "ACTIVE", "COMPLETED"] = "PLANNED"

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("End date cannot be before the start date.")

        return self


class CreateSprintRequest(SprintRequest):
    """Sprint creation request schema."""


class UpdateSprintRequest(SprintRequest):
    """Sprint update request schema."""
