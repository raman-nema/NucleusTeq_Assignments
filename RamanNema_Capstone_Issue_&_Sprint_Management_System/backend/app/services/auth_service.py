from app.models.user_model import UserModel
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password
from app.exceptions.custom_exceptions import UserAlreadyExistsException
from app.schemas.responses.auth_response import RegisterResponse


class AuthService:
    """Handles authentication-related business logic."""

    @staticmethod
    def register_user(request):

        # Check whether a user already exists with the same email.
        existing_user = UserRepository.find_by_email(request.email)

        # Stop registration if the email is already in use.
        if existing_user:
            raise UserAlreadyExistsException()

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
