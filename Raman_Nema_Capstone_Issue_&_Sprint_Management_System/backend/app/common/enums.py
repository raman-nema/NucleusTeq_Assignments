from enum import Enum


class Role(str, Enum):
    """Application roles used for authorization and access control."""

    ADMIN = "ADMIN"
    MEMBER = "MEMBER"
    VIEWER = "VIEWER"
