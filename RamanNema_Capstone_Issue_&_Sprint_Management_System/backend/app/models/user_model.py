from datetime import datetime


class UserModel:
    """Factory for user documents stored in the database."""

    @staticmethod
    def build(name: str, email: str, password: str, role: str) -> dict:
        """Build a user document with audit timestamps."""

        now = datetime.utcnow()

        return {
            "name": name,
            "email": email,
            "password": password,
            "role": role,
            "created_at": now,
            "updated_at": now,
        }
