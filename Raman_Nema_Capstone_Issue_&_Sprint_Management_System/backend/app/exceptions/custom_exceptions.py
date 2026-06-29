class UserAlreadyExistsException(Exception):
    """Raised when a user already exists."""

    pass


class InvalidCredentialsException(Exception):
    """Raised when login credentials are invalid."""

    pass


class UnauthorizedException(Exception):
    """Raised when authentication fails."""

    pass


class ExpiredTokenException(Exception):
    """Raised when authentication token has expired."""

    pass


class ForbiddenException(Exception):
    """Raised when user lacks permission."""

    pass


class ProjectAlreadyExistsException(Exception):
    """Raised when a project with the same name already exists."""

    pass


class ProjectNotFoundException(Exception):
    """Raised when the requested project does not exist."""

    pass
