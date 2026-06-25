from enum import Enum


class Role(str, Enum):
    """Application roles used for authorization and access control."""

    # Full administrative access across the application.
    ADMIN = "ADMIN"

    # Standard workspace access for active contributors.
    MEMBER = "MEMBER"

    # Read-only access for users who only need visibility.
    VIEWER = "VIEWER"
