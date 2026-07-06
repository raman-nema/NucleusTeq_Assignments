from app.core.database import database
from app.common.enums import Role
from app.core.security import hash_password


def seed_admin():
    """Create the default admin user when one is not already present."""
    existing_admin = database.users.find_one({"role": Role.ADMIN})

    if existing_admin:
        return

    database.users.insert_one(
        {
            "name": "Admin",
            "email": "admin@company.com",
            "password": hash_password("Admin@123"),
            "role": Role.ADMIN,
        }
    )
