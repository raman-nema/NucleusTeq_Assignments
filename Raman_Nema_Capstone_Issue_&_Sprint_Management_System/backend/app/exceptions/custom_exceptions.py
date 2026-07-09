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


class ProjectAlreadyExistsException(ConflictException):
    """Raised when a project already exists."""

    def __init__(self, message: str = "Project already exists"):
        super().__init__(message)


class SprintAlreadyExistsException(ConflictException):
    """Raised when a sprint already exists."""

    def __init__(self, message: str = "Sprint already exists"):
        super().__init__(message)


class ProjectNotFoundException(NotFoundException):
    """Raised when a project does not exist."""

    def __init__(self, message: str = "Project not found"):
        super().__init__(message)


class SprintNotFoundException(NotFoundException):
    """Raised when a sprint does not exist."""

    def __init__(self, message: str = "Sprint not found"):
        super().__init__(message)


class UserNotFoundException(NotFoundException):
    """Raised when a user does not exist."""

    def __init__(self, message: str = "User not found"):
        super().__init__(message)


class MemberAlreadyAssignedException(ConflictException):
    """Raised when assigning an existing project member."""

    def __init__(self, message: str = "Member already assigned"):
        super().__init__(message)


class MemberNotAssignedException(NotFoundException):
    """Raised when removing a user who is not assigned."""

    def __init__(self, message: str = "Member not assigned"):
        super().__init__(message)
