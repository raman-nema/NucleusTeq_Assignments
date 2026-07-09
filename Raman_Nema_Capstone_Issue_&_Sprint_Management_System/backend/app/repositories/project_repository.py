from bson import ObjectId
from app.core.database import database


class ProjectRepository:
    """Handles project database operations."""

    @staticmethod
    def create_project(project: dict):
        """Insert a new project document."""

        return database.projects.insert_one(project)

    @staticmethod
    def find_by_id(project_id: str):
        """Find a project by its ID."""

        return database.projects.find_one({"_id": ObjectId(project_id)})

    @staticmethod
    def find_by_name(name: str):
        """Find a project by its name."""

        return database.projects.find_one({"name": name})

    @staticmethod
    def find_all(skip: int = 0, limit: int = 10):
        """Retrieve a paginated list of projects."""

        return database.projects.find().sort("created_at", -1).skip(skip).limit(limit)

    @staticmethod
    def count_all():
        """Count all project documents."""

        return database.projects.count_documents({})

    @staticmethod
    def update_project(
        project_id: str,
        updated_data: dict,
    ):
        """Update an existing project."""

        return database.projects.update_one(
            {"_id": ObjectId(project_id)}, {"$set": updated_data}
        )

    @staticmethod
    def delete_project(project_id: str):
        """Delete a project."""

        return database.projects.delete_one({"_id": ObjectId(project_id)})
