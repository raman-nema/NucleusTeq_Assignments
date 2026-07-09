from fastapi import APIRouter

from app.schemas.requests.auth_request import RegisterRequest
from app.common.api_response import ApiResponse
from app.services.auth_service import AuthService
from app.schemas.requests.auth_request import RegisterRequest, LoginRequest

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=ApiResponse)
def register(request: RegisterRequest):
    """Register a new user account."""

    response = AuthService.register_user(request)

    # Return the shared API response format after successful registration.
    return ApiResponse(success=True, message=response.message, data=None)


@router.post("/login")
def login(request: LoginRequest):
    """Authenticate a user and return the generated access token."""

    response = AuthService.login_user(request)

    # Include token details in the response data for the authenticated session.
    return ApiResponse(
        success=True, message="Login successful", data=response.model_dump()
    )
