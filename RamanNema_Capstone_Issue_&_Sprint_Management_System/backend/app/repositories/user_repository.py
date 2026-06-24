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
