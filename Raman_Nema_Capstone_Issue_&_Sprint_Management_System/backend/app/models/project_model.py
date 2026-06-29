from datetime import datetime, timezone

class ProjectModel:
    """Creates project documents."""

    @staticmethod
    def build(
        name: str,
        description: str,
        created_by: str,
    ) -> dict:
        now = datetime.now(timezone.utc)

        # Build the project document for database insertion.
        return {
            "name": name,
            "description": description,
            "created_by": created_by,
            "created_at": now,
            "updated_at": now,
        }