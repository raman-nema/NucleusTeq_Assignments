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


class SprintAlreadyExistsException(Exception):
    """Raised when a sprint with the same name already exists."""

    def __init__(self):
        super().__init__("Sprint with this name already exists.")


class SprintNotFoundException(Exception):
    """Raised when a sprint is not found."""

    def __init__(self):
        super().__init__("Sprint not found.")


class UserNotFoundException(Exception):
    """Raised when a user is not found."""

    pass


class MemberAlreadyAssignedException(Exception):
    """Raised when the member is already assigned."""

    pass


class MemberNotAssignedException(Exception):
    """Raised when the member is not assigned."""

    pass


class IssueAlreadyExistsException(Exception):
    """Raised when an issue with the same title already exists."""

    pass


class IssueNotFoundException(Exception):
    """Raised when the requested issue does not exist."""

    pass
