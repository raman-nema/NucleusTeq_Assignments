class UserAlreadyExistsException(Exception):
    """Raised when a user already exists."""

    pass

class InvalidCredentialsException(Exception):
    """Raised when login credentials are invalid."""

    pass