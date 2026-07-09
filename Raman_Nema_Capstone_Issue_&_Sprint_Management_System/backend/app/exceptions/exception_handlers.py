from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from app.constants.message_constants import (
    INVALID_ISSUE_STATUS_TRANSITION_MESSAGE,
    ISSUE_ALREADY_EXISTS_MESSAGE,
    ISSUE_NOT_FOUND_MESSAGE,
    MEMBER_ALREADY_ASSIGNED_MESSAGE,
    MEMBER_NOT_ASSIGNED_MESSAGE,
    PROJECT_ALREADY_EXISTS_MESSAGE,
    PROJECT_HAS_SPRINTS_MESSAGE,
    PROJECT_NOT_FOUND_MESSAGE,
    SPRINT_ALREADY_EXISTS_MESSAGE,
    SPRINT_HAS_ISSUES_MESSAGE,
    SPRINT_NOT_FOUND_MESSAGE,
    USER_NOT_FOUND_MESSAGE,
)
from app.exceptions.custom_exceptions import (
    BadRequestException,
    ConflictException,
    ExpiredTokenException,
    ForbiddenException,
    InvalidCredentialsException,
    InvalidIssueStatusTransitionException,
    IssueAlreadyExistsException,
    IssueNotFoundException,
    MemberAlreadyAssignedException,
    MemberNotAssignedException,
    NotFoundException,
    ProjectAlreadyExistsException,
    ProjectHasSprintsException,
    ProjectNotFoundException,
    SprintAlreadyExistsException,
    SprintHasIssuesException,
    SprintNotFoundException,
    UnauthorizedException,
    UserNotFoundException,
)


def _error_response(status_code: int, message: str):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "data": None,
        },
    )


async def conflict_handler(request: Request, exc: ConflictException):
    """Return a conflict response for duplicate or conflicting resources."""

    return _error_response(409, exc.message)


async def invalid_credentials_handler(
    request: Request,
    exc: InvalidCredentialsException,
):
    """Return an unauthorized response for failed login attempts."""

    return _error_response(401, "Invalid email or password")


async def bad_request_handler(request: Request, exc: BadRequestException):
    """Return a bad request response for invalid request data."""

    return _error_response(400, exc.message)


async def not_found_handler(request: Request, exc: NotFoundException):
    """Return a not found response when a resource does not exist."""

    return _error_response(404, exc.message)


async def unauthorized_handler(request: Request, exc: UnauthorizedException):
    """Return an authentication failure response."""

    return _error_response(401, "Authentication required")


async def expired_token_handler(request: Request, exc: ExpiredTokenException):
    """Return an expired-token response."""

    return _error_response(401, "Token has expired")


async def forbidden_handler(request: Request, exc: ForbiddenException):
    """Return an authorization failure response."""

    return _error_response(403, "Access denied")


async def project_exists_handler(
    request: Request,
    exc: ProjectAlreadyExistsException,
):
    return _error_response(409, PROJECT_ALREADY_EXISTS_MESSAGE)


async def project_not_found_handler(
    request: Request,
    exc: ProjectNotFoundException,
):
    return _error_response(404, PROJECT_NOT_FOUND_MESSAGE)


async def project_has_sprints_handler(
    request: Request,
    exc: ProjectHasSprintsException,
):
    return _error_response(
        409,
        PROJECT_HAS_SPRINTS_MESSAGE,
    )


async def sprint_exists_handler(
    request: Request,
    exc: SprintAlreadyExistsException,
):
    return _error_response(409, SPRINT_ALREADY_EXISTS_MESSAGE)


async def sprint_not_found_handler(
    request: Request,
    exc: SprintNotFoundException,
):
    return _error_response(404, SPRINT_NOT_FOUND_MESSAGE)


async def sprint_has_issues_handler(
    request: Request,
    exc: SprintHasIssuesException,
):
    return _error_response(409, SPRINT_HAS_ISSUES_MESSAGE)


async def user_not_found_handler(request: Request, exc: UserNotFoundException):
    return _error_response(404, USER_NOT_FOUND_MESSAGE)


async def member_already_assigned_handler(
    request: Request,
    exc: MemberAlreadyAssignedException,
):
    return _error_response(409, MEMBER_ALREADY_ASSIGNED_MESSAGE)


async def member_not_assigned_handler(
    request: Request,
    exc: MemberNotAssignedException,
):
    return _error_response(404, MEMBER_NOT_ASSIGNED_MESSAGE)


async def issue_exists_handler(
    request: Request,
    exc: IssueAlreadyExistsException,
):
    return _error_response(409, ISSUE_ALREADY_EXISTS_MESSAGE)


async def issue_not_found_handler(
    request: Request,
    exc: IssueNotFoundException,
):
    return _error_response(404, ISSUE_NOT_FOUND_MESSAGE)


async def invalid_issue_status_transition_handler(
    request: Request,
    exc: InvalidIssueStatusTransitionException,
):
    return _error_response(400, INVALID_ISSUE_STATUS_TRANSITION_MESSAGE)


async def http_exception_handler(request: Request, exc: HTTPException):
    """Return FastAPI HTTPException errors in the API response shape."""

    return _error_response(exc.status_code, exc.detail)
