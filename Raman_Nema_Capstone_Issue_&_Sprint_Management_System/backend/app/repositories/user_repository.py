from bson import ObjectId
from bson.errors import InvalidId
from app.core.database import database


class UserRepository:
    """Data access layer for user records."""

    @staticmethod
    def find_by_email(email):
        """Find a user by email address."""

        return database.users.find_one({"email": email})

    @staticmethod
    def create_user(user):
        """Insert a new user document."""

        return database.users.insert_one(user)

    @staticmethod
    def find_by_id(user_id: str):
        """Find a user by MongoDB ObjectId."""

        return database.users.find_one(
            {
                "_id": ObjectId(user_id)
            }
        )

    @staticmethod
    def update_user(user_id: str, updated_data: dict):
        """Update a user document."""

        return database.users.update_one(
            {
                "_id": ObjectId(user_id),
            },
            {
                "$set": updated_data,
            },
        )

    @staticmethod
    def find_all(search: str | None = None):
        """Retrieve users, optionally filtered by name or ID."""

        query = {}

        if search:
            query = {
                "$or": [
                    {
                        "name": {
                            "$regex": search,
                            "$options": "i",
                        }
                    }
                ]
            }

            try:
                query["$or"].append(
                    {
                        "_id": ObjectId(search),
                    }
                )
            except InvalidId:
                pass

        return database.users.find(query).sort("created_at", -1)

    @staticmethod
    def count_all():
        """Count all users."""

        return database.users.count_documents({})
