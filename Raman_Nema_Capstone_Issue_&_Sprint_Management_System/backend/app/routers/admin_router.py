from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from app.common.api_response import ApiResponse
from app.dependencies.authorization import require_admin
from app.schemas.requests.admin_request import UpdateUserRequest
from app.services.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dashboard", response_model=ApiResponse)
def admin_dashboard(
    search: str | None = Query(None),
    current_user=Depends(require_admin),
):
    """Retrieve admin dashboard totals and users."""

    response = AdminService.get_dashboard(search)

    return ApiResponse(
        success=True,
        message="Admin dashboard retrieved successfully",
        data=response.model_dump(),
    )


@router.get("/users", response_model=ApiResponse)
def get_users(
    search: str | None = Query(None),
    role: str | None = Query(None),
    current_user=Depends(require_admin),
):
    """Retrieve users for the admin dashboard."""

    response = AdminService.get_users(
        search=search,
        role=role,
    )

    return ApiResponse(
        success=True,
        message="Users retrieved successfully",
        data=response.model_dump(),
    )


@router.put("/users/{user_id}", response_model=ApiResponse)
def update_user(
    user_id: str,
    request: UpdateUserRequest,
    current_user=Depends(require_admin),
):
    """Update a user from the admin dashboard."""

    response = AdminService.update_user(
        user_id,
        request,
    )

    return ApiResponse(
        success=True,
        message="User updated successfully",
        data=response.model_dump(),
    )
