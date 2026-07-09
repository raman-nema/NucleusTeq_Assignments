from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

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
    ProjectNotFoundException,
    SprintAlreadyExistsException,
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
    return _error_response(409, "Project already exists")


async def project_not_found_handler(
    request: Request,
    exc: ProjectNotFoundException,
):
    return _error_response(404, "Project not found")


async def sprint_exists_handler(
    request: Request,
    exc: SprintAlreadyExistsException,
):
    return _error_response(409, "Sprint already exists")


async def sprint_not_found_handler(
    request: Request,
    exc: SprintNotFoundException,
):
    return _error_response(404, "Sprint not found")


async def user_not_found_handler(request: Request, exc: UserNotFoundException):
    return _error_response(404, "User not found")


async def member_already_assigned_handler(
    request: Request,
    exc: MemberAlreadyAssignedException,
):
    return _error_response(409, "Member already assigned")


async def member_not_assigned_handler(
    request: Request,
    exc: MemberNotAssignedException,
):
    return _error_response(404, "Member not assigned")


async def issue_exists_handler(
    request: Request,
    exc: IssueAlreadyExistsException,
):
    return _error_response(409, "Issue already exists")


async def issue_not_found_handler(
    request: Request,
    exc: IssueNotFoundException,
):
    return _error_response(404, "Issue not found")


async def invalid_issue_status_transition_handler(
    request: Request,
    exc: InvalidIssueStatusTransitionException,
):
    return _error_response(400, "Issues in DONE state cannot move backward")


async def http_exception_handler(request: Request, exc: HTTPException):
    """Return FastAPI HTTPException errors in the API response shape."""

    return _error_response(exc.status_code, exc.detail)
