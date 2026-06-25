from fastapi import APIRouter

from app.schemas.requests.auth_request import RegisterRequest
from app.common.api_response import ApiResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=ApiResponse)
def register(request: RegisterRequest):
    """Register a new user account."""

    response = AuthService.register_user(request)

    return ApiResponse(success=True, message=response.message, data=None)
