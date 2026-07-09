from app.constants.message_constants import (
    SPRINT_ALREADY_EXISTS_MESSAGE,
    SPRINT_NOT_FOUND_MESSAGE,
)


class ConflictException(Exception):
    """Raised when a request conflicts with an existing resource."""

    def __init__(self, message: str = "Resource already exists"):
        self.message = message
        super().__init__(message)


class UserAlreadyExistsException(Exception):
    pass


class InvalidCredentialsException(Exception):
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
    pass


class ExpiredTokenException(Exception):
    pass


class ForbiddenException(Exception):
    pass


class ProjectAlreadyExistsException(Exception):
    pass


class ProjectNotFoundException(Exception):
    pass


class ProjectHasSprintsException(Exception):
    pass


class SprintAlreadyExistsException(Exception):
    def __init__(self):
        super().__init__(SPRINT_ALREADY_EXISTS_MESSAGE)


class SprintNotFoundException(Exception):
    def __init__(self):
        super().__init__(SPRINT_NOT_FOUND_MESSAGE)


class SprintHasIssuesException(Exception):
    pass


class UserNotFoundException(Exception):
    pass


class MemberAlreadyAssignedException(Exception):
    pass


class MemberNotAssignedException(Exception):
    pass


class IssueAlreadyExistsException(Exception):
    pass


class IssueNotFoundException(Exception):
    pass


class InvalidIssueStatusTransitionException(Exception):
    pass
