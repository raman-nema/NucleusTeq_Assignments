import base64
import binascii

import bcrypt

PASSWORD_ENCODING_PREFIX = "encoded:"


def hash_password(password: str):
    """Return a bcrypt hash for a plain-text password."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain-text password against its hashed version."""
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def decode_password(password: str):
    """Decode frontend-encoded passwords while accepting existing plain values."""

    if not password.startswith(PASSWORD_ENCODING_PREFIX):
        return password

    encoded_password = password.removeprefix(PASSWORD_ENCODING_PREFIX)

    try:
        return base64.b64decode(encoded_password, validate=True).decode("utf-8")
    except (binascii.Error, UnicodeDecodeError) as error:
        raise ValueError("Invalid encoded password.") from error
