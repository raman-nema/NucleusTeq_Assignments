from datetime import datetime


class UserModel:
    @staticmethod
    def build(name: str, email: str, password: str, role: str) -> dict:
        now = datetime.utcnow()
        return {
            "name": name,
            "email": email,
            "password": password,
            "role": role,
            "created_at": now,
            "updated_at": now,
        }
