from datetime import datetime
from fastapi import Header
from app.repositories.token_repository import TokenRepository
from app.repositories.user_repository import UserRepository
from app.exceptions.custom_exceptions import (
    UnauthorizedException,
    ExpiredTokenException,
)


def get_current_user(
    authorization: str = Header(None),
):
    """Returns the currently authenticated user."""

    if authorization is None:
        raise UnauthorizedException()

    if not authorization.startswith("Bearer "):
        raise UnauthorizedException()

    token = authorization.replace(
        "Bearer ",
        "",
    )

    token_document = TokenRepository.find_by_token(token)

    if token_document is None:
        raise UnauthorizedException()

    if token_document["expires_at"] < datetime.utcnow():
        raise ExpiredTokenException()

    user = UserRepository.find_by_id(token_document["user_id"])

    if user is None:
        raise UnauthorizedException()

    return user
