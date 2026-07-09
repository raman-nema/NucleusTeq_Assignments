import re

from pydantic import (
    BaseModel,
    Field,
    field_validator,
)
from app.exceptions.custom_exceptions import BadRequestException


class CreateProjectRequest(BaseModel):
    """Project creation request schema."""

    name: str = Field(
        min_length=3,
        max_length=100,
    )

    description: str = Field(
        min_length=10,
        max_length=500,
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):

        # Remove leading and trailing whitespace.
        value = value.strip()

        # Regular expression for project name validation.
        project_name_pattern = r"^[A-Za-z0-9][A-Za-z0-9\s_-]*$"

        if not re.match(project_name_pattern, value):
            raise BadRequestException("Project name contains invalid characters.")

        return value

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str):

        # Remove leading and trailing whitespace.
        return value.strip()


class UpdateProjectRequest(CreateProjectRequest):
    """Project update request schema."""

    pass
