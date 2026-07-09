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
    def find_all_by_project(
        project_id: str,
        status: str | None = None,
    ):
        """Retrieve all issues for a project."""

        query = {
            "project_id": ObjectId(project_id),
        }

        if status:
            query["status"] = status

        return database.issues.find(query).sort(
            "created_at",
            -1,
        )

    @staticmethod
    def count_by_project(
        project_id: str,
        status: str | None = None,
    ):
        """Count issues for a project."""

        query = {
            "project_id": ObjectId(project_id),
        }

        if status:
            query["status"] = status

        return database.issues.count_documents(query)

    @staticmethod
    def count_by_sprint(sprint_id: str):
        """Count issues assigned to a sprint."""

        return database.issues.count_documents(
            {
                "sprint_id": ObjectId(sprint_id),
            }
        )

    @staticmethod
    def count_by_parent(parent_id: str):
        """Count issues linked to a parent issue."""

        return database.issues.count_documents(
            {
                "parent_id": ObjectId(parent_id),
            }
        )

    @staticmethod
    def count_all():
        """Count all issues."""

        return database.issues.count_documents({})

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
    def add_comment(issue_id: str, comment: dict):
        """Append a comment to an issue."""

        return database.issues.update_one(
            {
                "_id": ObjectId(issue_id),
            },
            {
                "$push": {
                    "comments": comment,
                },
            },
        )

    @staticmethod
    def update_comment(issue_id: str, comment_id: str, updated_data: dict):
        """Update an embedded issue comment."""

        return database.issues.update_one(
            {
                "_id": ObjectId(issue_id),
                "comments._id": ObjectId(comment_id),
            },
            {
                "$set": {
                    "comments.$.text": updated_data["text"],
                    "comments.$.updated_at": updated_data["updated_at"],
                    "updated_at": updated_data["updated_at"],
                },
            },
        )

    @staticmethod
    def delete_comment(issue_id: str, comment_id: str):
        """Remove a comment from an issue."""

        return database.issues.update_one(
            {
                "_id": ObjectId(issue_id),
            },
            {
                "$pull": {
                    "comments": {
                        "_id": ObjectId(comment_id),
                    },
                },
            },
        )

    @staticmethod
    def find_all_by_sprint(sprint_id: str):
        """Retrieve all issues for a sprint."""

        query = {
            "sprint_id": ObjectId(sprint_id),
        }

        return database.issues.find(
            query
        ).sort(
            "created_at",
            -1,
        )
