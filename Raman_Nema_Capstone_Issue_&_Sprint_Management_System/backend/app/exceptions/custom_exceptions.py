class ConflictException(Exception):
    """Raised when a request conflicts with an existing resource."""

    def __init__(self, message: str = "Resource already exists"):
        self.message = message
        super().__init__(message)


class InvalidCredentialsException(Exception):
    """Raised when login credentials are invalid."""

    pass


class BadRequestException(Exception):
    """Raised when request data is invalid."""

    def __init__(self, message: str = "Bad request"):
        self.message = message
        super().__init__(message)


class NotFoundException(Exception):
    """Raised when a requested resource does not exist."""

    def __init__(self, message: str = "Resource not found"):
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
