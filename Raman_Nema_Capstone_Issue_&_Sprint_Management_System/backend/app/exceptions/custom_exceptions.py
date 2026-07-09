class UserAlreadyExistsException(Exception):
    """Raised when a user already exists."""

    pass


class InvalidCredentialsException(Exception):
    """Raised when login credentials are invalid."""

    pass


class BadRequestException(Exception):
    """Raised when request data is invalid."""

    def __init__(self, message: str = "Bad request"):
        self.message = message
        super().__init__(message)


class UnauthorizedException(Exception):
    """Raised when authentication fails."""

    pass


class ExpiredTokenException(Exception):
    """Raised when authentication token has expired."""

    pass


class ForbiddenException(Exception):
    """Raised when user lacks permission."""

    pass
