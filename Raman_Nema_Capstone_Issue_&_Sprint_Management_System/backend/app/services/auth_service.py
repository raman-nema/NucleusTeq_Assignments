from app.models.user_model import UserModel
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password
from app.constants.message_constants import USER_EMAIL_ALREADY_EXISTS_MESSAGE
from app.exceptions.custom_exceptions import ConflictException
from app.schemas.responses.auth_response import RegisterResponse
from app.common.api_response import ApiResponse
import uuid

from datetime import datetime
from datetime import timedelta

from app.core.security import hash_password, verify_password

from app.models.token_model import TokenModel

from app.repositories.token_repository import TokenRepository

from app.schemas.responses.auth_response import LoginResponse, LogoutResponse

from app.exceptions.custom_exceptions import InvalidCredentialsException


class AuthService:
    """Handles authentication-related business logic."""

    @staticmethod
    def register_user(request):

        # Check whether a user already exists with the same email.
        existing_user = UserRepository.find_by_email(request.email)

        # Stop registration if the email is already in use.
        if existing_user:
            raise ConflictException(USER_EMAIL_ALREADY_EXISTS_MESSAGE)

        # Hash the password before storing it.
        hashed_password = hash_password(request.password)

        # Build the user document for database insertion.
        user = UserModel.build(
            name=request.name,
            email=request.email,
            password=hashed_password,
            role=request.role.value,
        )

        # Save the new user record.
        UserRepository.create_user(user)

        return RegisterResponse(message="User registered successfully")

    @staticmethod
    def login_user(request):

        # Look up the user by email before checking the submitted password.
        user = UserRepository.find_by_email(request.email)

        # Reject login attempts when the email is not registered.
        if not user:
            raise InvalidCredentialsException()

        # Reject login attempts when the submitted password does not match.
        if not verify_password(request.password, user["password"]):
            raise InvalidCredentialsException()

        # Remove older tokens so only the latest login session remains active.
        TokenRepository.delete_user_tokens(str(user["_id"]))

        # Create a new token value and set a 24-hour expiry time.
        token = str(uuid.uuid4())

        expires_at = datetime.utcnow() + timedelta(hours=24)

        # Build and persist the token document for later authentication checks.
        token_document = TokenModel.build(
            user_id=str(user["_id"]),
            email=user["email"],
            token=token,
            expires_at=expires_at,
        )

        TokenRepository.create_token(token_document)

        # Return token details to the router for the login API response.
        return LoginResponse(
            access_token=token, role=user["role"], expires_at=expires_at
        )

    @staticmethod
    def logout_user(token: str):
        """Logout the authenticated user."""

        token_document = TokenRepository.find_by_token(token)

        if not token_document:
            raise InvalidCredentialsException()

        TokenRepository.delete_token(token)
        return LogoutResponse(message="Logout successful")
