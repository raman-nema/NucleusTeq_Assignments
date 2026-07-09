from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from app.exceptions.custom_exceptions import (
    BadRequestException,
    ConflictException,
    ExpiredTokenException,
    ForbiddenException,
    InvalidCredentialsException,
    NotFoundException,
    UnauthorizedException,
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
    """Return an authentication failure response."""

    return JSONResponse(
        status_code=401,
        content={
            "success": False,
            "message": "Authentication required",
            "data": None,
        },
    )


async def expired_token_handler(request: Request, exc: ExpiredTokenException):
    """Return an expired-token response."""

    return JSONResponse(
        status_code=401,
        content={
            "success": False,
            "message": "Token has expired",
            "data": None,
        },
    )


async def forbidden_handler(request: Request, exc: ForbiddenException):
    """Return an authorization failure response."""

    return JSONResponse(
        status_code=403,
        content={
            "success": False,
            "message": "Access denied",
            "data": None,
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Return FastAPI HTTPException errors in the API response shape."""

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "data": None,
        },
    )
