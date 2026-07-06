from fastapi import Depends
from app.common.enums import Role
from app.exceptions.custom_exceptions import ForbiddenException
from app.dependencies.authentication import get_current_user


def require_admin(current_user=Depends(get_current_user)):
    """Allows only ADMIN users."""
    if current_user["role"] != Role.ADMIN.value:
        raise ForbiddenException()
    return current_user


def require_member(current_user=Depends(get_current_user)):
    """Allows only MEMBER users."""
    if current_user["role"] != Role.MEMBER.value:
        raise ForbiddenException()
    return current_user


def require_viewer(current_user=Depends(get_current_user)):
    """Allows only VIEWER users."""
    if current_user["role"] != Role.VIEWER.value:
        raise ForbiddenException()
    return current_user


def require_admin_or_member(current_user=Depends(get_current_user)):
    """Allows ADMIN and MEMBER."""
    if current_user["role"] not in [Role.ADMIN.value, Role.MEMBER.value]:
        raise ForbiddenException()
    return current_user
