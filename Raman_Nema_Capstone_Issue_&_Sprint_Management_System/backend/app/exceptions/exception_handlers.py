from fastapi.responses import JSONResponse
from fastapi import Request

from app.exceptions.custom_exceptions import UserAlreadyExistsException


async def user_exists_handler(request: Request, exc: UserAlreadyExistsException):
    """Return a conflict response for duplicate user registration attempts."""

    return JSONResponse(
        status_code=409,
        content={"success": False, "message": "User_Email already exists", "data": None},
    )
