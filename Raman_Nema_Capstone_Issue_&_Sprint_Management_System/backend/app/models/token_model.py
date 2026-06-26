from datetime import datetime
from datetime import datetime, timezone

now = datetime.now(timezone.utc)


class TokenModel:
    """Creates authentication token documents."""

    @staticmethod
    def build(user_id: str, email: str, token: str, expires_at: datetime) -> dict:

        now = datetime.utcnow()

        # Store token metadata in the same shape expected by the token repository.
        return {
            "user_id": user_id,
            "email": email,
            "token": token,
            "created_at": now,
            "expires_at": expires_at,
        }
