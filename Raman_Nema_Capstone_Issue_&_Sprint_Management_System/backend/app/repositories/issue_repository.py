from bson import ObjectId

from app.core.database import database


class IssueRepository:
    """Handles issue database operations."""

    @staticmethod
    def create_issue(issue: dict):
        """Insert a new issue document."""

        return database.issues.insert_one(issue)

    @staticmethod
    def find_by_id(issue_id: str):
        """Find an issue by its ID."""

        return database.issues.find_one(
            {
                "_id": ObjectId(issue_id),
            }
        )

    @staticmethod
    def find_by_title(
        project_id: str,
        title: str,
    ):
        """Find an issue by title within a project."""

        return database.issues.find_one(
            {
                "project_id": ObjectId(project_id),
                "title": title,
            }
        )

    @staticmethod
    def find_all_by_project(project_id: str):
        """Retrieve all issues for a project."""

        return database.issues.find(
            {
                "project_id": ObjectId(project_id),
            }
        ).sort(
            "created_at",
            -1,
        )

    @staticmethod
    def count_by_project(project_id: str):
        """Count issues for a project."""

        return database.issues.count_documents(
            {
                "project_id": ObjectId(project_id),
            }
        )

    @staticmethod
    def update_issue(
        issue_id: str,
        updated_data: dict,
    ):
        """Update an existing issue."""

        return database.issues.update_one(
            {
                "_id": ObjectId(issue_id),
            },
            {
                "$set": updated_data,
            },
        )

    @staticmethod
    def delete_issue(issue_id: str):
        """Delete an issue."""

        return database.issues.delete_one(
            {
                "_id": ObjectId(issue_id),
            }
        )

    @staticmethod
    def find_all_by_sprint(sprint_id: str):
        """Retrieve all issues for a sprint."""

        return database.issues.find(
            {
                "sprint_id": ObjectId(sprint_id),
            }
        ).sort(
            "created_at",
            -1,
        )
