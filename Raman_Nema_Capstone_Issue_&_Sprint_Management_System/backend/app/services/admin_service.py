from datetime import datetime

from app.constants.message_constants import USER_EMAIL_ALREADY_EXISTS_MESSAGE
from app.exceptions.custom_exceptions import (
    ConflictException,
    UserNotFoundException,
)
from app.repositories.issue_repository import IssueRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.sprint_repository import SprintRepository
from app.repositories.user_repository import UserRepository
from app.schemas.requests.admin_request import UpdateUserRequest
from app.schemas.responses.admin_response import (
    AdminDashboardResponse,
    AdminTotalsResponse,
    AdminUserListResponse,
    AdminUserResponse,
)


class AdminService:
    """Handles admin dashboard and user management business logic."""

    @staticmethod
    def _build_user_response(user: dict):
        """Build an admin user response from a Mongo document."""

        return AdminUserResponse(
            id=str(user["_id"]),
            name=user["name"],
            email=user["email"],
            role=user["role"],
            created_at=user.get("created_at"),
            updated_at=user.get("updated_at"),
        )

    @staticmethod
    def get_dashboard(search: str | None = None):
        """Retrieve dashboard totals and filtered users."""

        users = [
            AdminService._build_user_response(user)
            for user in UserRepository.find_all(search=search)
        ]

        return AdminDashboardResponse(
            totals=AdminTotalsResponse(
                projects=ProjectRepository.count_all(),
                sprints=SprintRepository.count_all(),
                issues=IssueRepository.count_all(),
                users=UserRepository.count_all(),
            ),
            users=users,
        )

    @staticmethod
    def get_users(
        search: str | None = None,
        role: str | None = None,
    ):
        """Retrieve users filtered by search text or role."""

        return AdminUserListResponse(
            users=[
                AdminService._build_user_response(user)
                for user in UserRepository.find_all(
                    search=search,
                    role=role,
                )
            ]
        )

    @staticmethod
    def update_user(user_id: str, request: UpdateUserRequest):
        """Update an existing user."""

        user = UserRepository.find_by_id(user_id)

        if not user:
            raise UserNotFoundException()

        existing_user = UserRepository.find_by_email(request.email)

        if existing_user and str(existing_user["_id"]) != user_id:
            raise ConflictException(USER_EMAIL_ALREADY_EXISTS_MESSAGE)

        updated_data = {
            "name": request.name,
            "email": str(request.email),
            "updated_at": datetime.utcnow(),
        }

        UserRepository.update_user(
            user_id,
            updated_data,
        )

        user.update(updated_data)

        return AdminService._build_user_response(user)
