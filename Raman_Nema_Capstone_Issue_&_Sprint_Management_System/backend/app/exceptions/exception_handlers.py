from fastapi.responses import JSONResponse
from fastapi import Request
from app.exceptions.custom_exceptions import (
    UserAlreadyExistsException,
    InvalidCredentialsException,
    UnauthorizedException,
    ExpiredTokenException,
    ForbiddenException,
    ProjectAlreadyExistsException,
    ProjectNotFoundException,
    SprintAlreadyExistsException,
    SprintNotFoundException,
    UserNotFoundException,
    MemberAlreadyAssignedException,
    MemberNotAssignedException,
    IssueAlreadyExistsException,
    IssueNotFoundException,
    InvalidIssueStatusTransitionException,
)


async def user_exists_handler(request: Request, exc: UserAlreadyExistsException):
    """Return a conflict response for duplicate user registration attempts."""

    return JSONResponse(
        status_code=409,
        content={
            "success": False,
            "message": "User_Email already exists",
            "data": None,
        },
    )


async def invalid_credentials_handler(
    request: Request, exc: InvalidCredentialsException
):
    """Return an unauthorized response for failed login attempts."""

    # Keep authentication error responses consistent with the API response shape.
    return JSONResponse(
        status_code=401,
        content={
            "success": False,
            "message": "Invalid email or password",
            "data": None,
        },
    )


async def unauthorized_handler(request: Request, exc: UnauthorizedException):

    return JSONResponse(
        status_code=401,
        content={"success": False, "message": "Authentication required", "data": None},
    )


async def expired_token_handler(request: Request, exc: ExpiredTokenException):

    return JSONResponse(
        status_code=401,
        content={"success": False, "message": "Token has expired", "data": None},
    )


async def forbidden_handler(request: Request, exc: ForbiddenException):

    return JSONResponse(
        status_code=403,
        content={"success": False, "message": "Access denied", "data": None},
    )


async def project_exists_handler(request: Request, exc: ProjectAlreadyExistsException):
    """Return a conflict response for duplicate project creation."""

    return JSONResponse(
        status_code=409,
        content={
            "success": False,
            "message": "Project already exists",
            "data": None,
        },
    )


async def project_not_found_handler(request: Request, exc: ProjectNotFoundException):
    """Return a not found response when the project does not exist."""

    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": "Project not found",
            "data": None,
        },
    )


async def sprint_exists_handler(request: Request, exc: SprintAlreadyExistsException):
    """Return a conflict response for duplicate sprint creation."""

    return JSONResponse(
        status_code=409,
        content={
            "success": False,
            "message": "Sprint already exists",
            "data": None,
        },
    )


async def sprint_not_found_handler(request: Request, exc: SprintNotFoundException):
    """Return a not found response when the sprint does not exist."""

    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": "Sprint not found",
            "data": None,
        },
    )


async def user_not_found_handler(request: Request, exc: UserNotFoundException):

    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": "User not found",
            "data": None,
        },
    )


async def member_already_assigned_handler(
    request: Request, exc: MemberAlreadyAssignedException
):

    return JSONResponse(
        status_code=409,
        content={
            "success": False,
            "message": "Member already assigned",
            "data": None,
        },
    )


async def member_not_assigned_handler(
    request: Request, exc: MemberNotAssignedException
):

    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": "Member not assigned",
            "data": None,
        },
    )


async def issue_exists_handler(
    request: Request,
    exc: IssueAlreadyExistsException,
):
    return JSONResponse(
        status_code=409,
        content={
            "success": False,
            "message": "Issue already exists",
            "data": None,
        },
    )


async def issue_not_found_handler(
    request: Request,
    exc: IssueNotFoundException,
):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": "Issue not found",
            "data": None,
        },
    )


async def invalid_issue_status_transition_handler(
    request: Request,
    exc: InvalidIssueStatusTransitionException,
):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": "Issues in DONE state cannot move backward",
            "data": None,
        },
    )
