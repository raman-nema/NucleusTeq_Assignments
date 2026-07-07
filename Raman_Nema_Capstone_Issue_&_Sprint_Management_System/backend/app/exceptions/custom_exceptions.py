class UserAlreadyExistsException(Exception):
    pass


class InvalidCredentialsException(Exception):
    pass


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
        super().__init__("Sprint with this name already exists.")


class SprintNotFoundException(Exception):
    def __init__(self):
        super().__init__("Sprint not found.")


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
