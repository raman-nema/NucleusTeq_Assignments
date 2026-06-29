from fastapi import APIRouter
from fastapi import Header
from app.common.api_response import ApiResponse
from app.schemas.requests.auth_request import (
    RegisterRequest,
    LoginRequest,
)
from app.services.auth_service import AuthService
from app.exceptions.custom_exceptions import (
    UnauthorizedException,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post("/register", response_model=ApiResponse)
def register(request: RegisterRequest):
    """Register a new user account."""

    response = AuthService.register_user(request)

    return ApiResponse(
        success=True,
        message=response.message,
        data=None,
    )

@router.post("/login", response_model=ApiResponse)
def login(request: LoginRequest):
    """Authenticate a user and return the generated access token."""

    response = AuthService.login_user(request)

    return ApiResponse(
        success=True,
        message="Login successful",
        data=response.model_dump(),
    )

@router.post("/logout", response_model=ApiResponse)
def logout(
    authorization: str = Header(None),
):
    """Logout the authenticated user."""

    if authorization is None or not authorization.startswith("Bearer "):
        raise UnauthorizedException()

    token = authorization.replace("Bearer ", "")

    response = AuthService.logout_user(token)

    return ApiResponse(
        success=True,
        message=response.message,
        data=None,
    )
