from fastapi.responses import JSONResponse
from fastapi import Request
from app.exceptions.custom_exceptions import (
    ConflictException,
    InvalidCredentialsException,
    BadRequestException,
    NotFoundException,
    UnauthorizedException,
    ExpiredTokenException,
    ForbiddenException,
)


async def conflict_handler(request: Request, exc: ConflictException):
    """Return a conflict response for duplicate or conflicting resources."""

    return JSONResponse(
        status_code=409,
        content={
            "success": False,
            "message": exc.message,
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


async def bad_request_handler(request: Request, exc: BadRequestException):
    """Return a bad request response for invalid request data."""

    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": exc.message,
            "data": None,
        },
    )


async def not_found_handler(request: Request, exc: NotFoundException):
    """Return a not found response when a resource does not exist."""

    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": exc.message,
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
