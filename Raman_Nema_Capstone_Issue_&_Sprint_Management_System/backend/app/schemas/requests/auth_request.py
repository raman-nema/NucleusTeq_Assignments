import re
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
)
from app.common.enums import Role
from app.core.security import decode_password


class RegisterRequest(BaseModel):
    """User registration request schema."""

    name: str = Field(
        min_length=3,
        max_length=50,
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=20,
    )

    role: Role

    @field_validator("email")
    @classmethod
    def validate_company_email(cls, value: EmailStr):
        if not str(value).endswith("@company.com"):
            raise ValueError("Only company email addresses are allowed.")

        return value

    @field_validator("password", mode="before")
    @classmethod
    def decode_encoded_password(cls, value: str):
        return decode_password(value)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):

        # Require uppercase, lowercase, number, special character, and 8–20 characters.
        password_pattern = (
            r"^(?=.*[a-z])" r"(?=.*[A-Z])" r"(?=.*\d)" r"(?=.*[@$!%*?&]).{8,20}$"
        )

        if not re.match(password_pattern, value):
            raise ValueError(
                "Password must be 8-20 characters long and contain an uppercase letter, "
                "lowercase letter, number and special character."
            )
        return value


class LoginRequest(BaseModel):
    """User login request schema."""

    email: EmailStr

    password: str = Field(
        min_length=8,
    )

    @field_validator("password", mode="before")
    @classmethod
    def decode_encoded_password(cls, value: str):
        return decode_password(value)

    @field_validator("email")
    @classmethod
    def validate_company_email(cls, value: EmailStr):
        if not str(value).endswith("@company.com"):
            raise ValueError("Only company email addresses are allowed.")

        return value
