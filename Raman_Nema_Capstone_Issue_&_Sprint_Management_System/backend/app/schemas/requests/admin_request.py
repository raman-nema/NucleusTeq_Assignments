from pydantic import BaseModel, EmailStr, Field, field_validator


class UpdateUserRequest(BaseModel):
    """User fields an admin can update from the dashboard."""

    name: str = Field(
        min_length=3,
        max_length=50,
    )

    email: EmailStr

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):
        return value.strip()

    @field_validator("email")
    @classmethod
    def validate_company_email(cls, value: EmailStr):
        if not str(value).endswith("@company.com"):
            raise ValueError("Only company email addresses are allowed.")

        return value
