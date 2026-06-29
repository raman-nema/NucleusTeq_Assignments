from fastapi.responses import JSONResponse
from fastapi import Request
from app.exceptions.custom_exceptions import (
    UserAlreadyExistsException,
    InvalidCredentialsException,
    UnauthorizedException,
    ExpiredTokenException,
    ForbiddenException,
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
