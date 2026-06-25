import bcrypt


def hash_password(password: str):
    """Return a bcrypt hash for a plain-text password."""

    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
