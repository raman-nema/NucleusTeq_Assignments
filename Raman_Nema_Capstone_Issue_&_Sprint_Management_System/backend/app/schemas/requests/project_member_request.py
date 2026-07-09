from pydantic import BaseModel


class AssignMemberRequest(BaseModel):
    """Project member assignment request schema."""

    user_id: str