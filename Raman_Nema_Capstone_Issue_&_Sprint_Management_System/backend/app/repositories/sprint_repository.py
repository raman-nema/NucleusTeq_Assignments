from bson import ObjectId
from app.core.database import database


class SprintRepository:
    """Handles sprint database operations."""

    @staticmethod
    def create_sprint(sprint: dict):
        """Insert a new sprint document."""

        # Save the sprint document.
        return database.sprints.insert_one(sprint)

    @staticmethod
    def find_by_id(sprint_id: str):
        """Find a sprint by its ID."""

        # Retrieve sprint using its ID.
        return database.sprints.find_one(
            {
                "_id": ObjectId(sprint_id),
            }
        )

    @staticmethod
    def find_by_name(
        project_id: str,
        name: str,
    ):
        """Find a sprint by its name within a project."""

        # Check for an existing sprint with the same name.
        return database.sprints.find_one(
            {
                "project_id": ObjectId(project_id),
                "name": name,
            }
        )

    @staticmethod
    def find_all_by_project(project_id: str):
        """Retrieve all sprints for a project."""

        # Return project sprints in descending creation order.
        return database.sprints.find(
            {
                "project_id": ObjectId(project_id),
            }
        ).sort("created_at", -1)

    @staticmethod
    def update_sprint(
        sprint_id: str,
        updated_data: dict,
    ):
        """Update an existing sprint."""

        # Apply the provided field updates.
        return database.sprints.update_one(
            {
                "_id": ObjectId(sprint_id),
            },
            {
                "$set": updated_data,
            },
        )

    @staticmethod
    def delete_sprint(sprint_id: str):
        """Delete a sprint."""

        # Remove the sprint by ID.
        return database.sprints.delete_one(
            {
                "_id": ObjectId(sprint_id),
            }
        )
