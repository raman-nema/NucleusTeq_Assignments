from fastapi import APIRouter
from fastapi import Depends
from app.common.api_response import ApiResponse
from app.constants.message_constants import ADMIN_DASHBOARD_MESSAGE
from app.dependencies.authorization import require_admin
from app.schemas.responses.admin_response import AdminDashboardResponse

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dashboard", response_model=ApiResponse)
def admin_dashboard(current_user=Depends(require_admin)):
    """
    Admin dashboard.
    Accessible only by ADMIN users.
    """

    response = AdminDashboardResponse(
        name=current_user["name"],
        email=current_user["email"],
        role=current_user["role"],
    )

    return ApiResponse(
        success=True,
        message=ADMIN_DASHBOARD_MESSAGE,
        data=response.model_dump(),
    )
