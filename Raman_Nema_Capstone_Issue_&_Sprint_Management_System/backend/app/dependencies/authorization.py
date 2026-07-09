from fastapi import Depends
from app.common.enums import Role
from app.exceptions.custom_exceptions import ForbiddenException
from app.dependencies.authentication import get_current_user


# These dependencies first authenticate the request, then verify the user's role.
def require_admin(current_user=Depends(get_current_user)):
    """
    Allows only ADMIN users.
    """

    # Block the request if the authenticated user is not an admin.
    if current_user["role"] != Role.ADMIN.value:

        raise ForbiddenException()

    return current_user


def require_manager(current_user=Depends(get_current_user)):
    """
    Allows only MANAGER users.
    """

    # Block the request if the authenticated user is not a manager.
    if current_user["role"] != Role.MANAGER.value:

        raise ForbiddenException()

    return current_user


def require_viewer(current_user=Depends(get_current_user)):
    """
    Allows only VIEWER users.
    """

    # Block the request if the authenticated user is not a viewer.
    if current_user["role"] != Role.VIEWER.value:

        raise ForbiddenException()

    return current_user


def require_admin_or_manager(current_user=Depends(get_current_user)):
    """
    Allows ADMIN and MANAGER.
    """

    # Allow shared access for admin and manager roles only.
    if current_user["role"] not in [Role.ADMIN.value, Role.MANAGER.value]:

        raise ForbiddenException()

    return current_user
