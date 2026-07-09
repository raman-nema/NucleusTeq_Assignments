from datetime import datetime
from bson import ObjectId


class IssueModel:
    """Issue document model."""

    @staticmethod
    def build(
        project_id: str,
        sprint_id: str | None,
        title: str,
        description: str,
        priority: str,
        type: str,
        status: str,
        assignee: str,
        reporter: str,
    ):
        """Create an issue document."""

        current_time = datetime.utcnow()

        return {
            "project_id": ObjectId(project_id),
            "sprint_id": (ObjectId(sprint_id) if sprint_id else None),
            "title": title,
            "description": description,
            "priority": priority,
            "type": type,
            "status": status,
            "assignee": assignee,
            "reporter": reporter,
            "comments": [],
            "created_at": current_time,
            "updated_at": current_time,
        }
