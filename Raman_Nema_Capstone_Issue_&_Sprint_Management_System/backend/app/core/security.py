import bcrypt


def hash_password(password: str):
    """Return a bcrypt hash for a plain-text password."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain-text password against its hashed version."""
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
