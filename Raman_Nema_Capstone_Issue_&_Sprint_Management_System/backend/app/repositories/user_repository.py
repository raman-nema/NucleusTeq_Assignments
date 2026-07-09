from bson import ObjectId
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
