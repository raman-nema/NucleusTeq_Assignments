from datetime import datetime, timezone
from bson import ObjectId


class ProjectModel:
    """Creates project documents."""

    @staticmethod
    def build(
        name: str,
        description: str,
        created_by: str,
    ) -> dict:
        """Build a project document."""

        now = datetime.now(timezone.utc)

        return {
            "name": name,
            "description": description,
            "created_by": created_by,
            "members": [
                ObjectId(created_by),
            ],
            "created_at": now,
            "updated_at": now,
        }