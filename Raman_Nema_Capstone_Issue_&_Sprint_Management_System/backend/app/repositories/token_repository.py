from app.core.database import database
from datetime import datetime


class TokenRepository:
    """Handles authentication token operations."""

    @staticmethod
    def create_token(token: dict):

        # Persist a newly issued authentication token document.
        return database.auth_tokens.insert_one(token)

    @staticmethod
    def find_by_token(token: str):

        return database.auth_tokens.find_one({"token": token})

    @staticmethod
    def delete_token(token: str):

        return database.auth_tokens.delete_one({"token": token})

    @staticmethod
    def delete_user_tokens(user_id: str):

        # Remove all active tokens for a user, such as during logout from all sessions.
        return database.auth_tokens.delete_many({"user_id": user_id})

    @staticmethod
    def delete_expired_tokens():
        """Delete expired authentication tokens."""

        return database.auth_tokens.delete_many(
            {"expires_at": {"$lt": datetime.utcnow()}}
        )
