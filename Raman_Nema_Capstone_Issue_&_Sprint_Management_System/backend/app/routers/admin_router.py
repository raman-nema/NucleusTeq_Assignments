from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from app.dependencies.authorization import require_admin
from app.exceptions.custom_exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
)
from app.repositories.issue_repository import IssueRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.sprint_repository import SprintRepository
from app.repositories.user_repository import UserRepository
from app.schemas.requests.admin_request import UpdateUserRequest

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dashboard")
def admin_dashboard(
    search: str | None = Query(None),
    current_user=Depends(require_admin),
):
    users = []

    for user in UserRepository.find_all(search):
        users.append(
            {
                "id": str(user["_id"]),
                "name": user["name"],
                "email": user["email"],
                "role": user["role"],
                "created_at": user.get("created_at"),
                "updated_at": user.get("updated_at"),
            }
        )

    return {
        "success": True,
        "message": "Admin dashboard retrieved successfully",
        "data": {
            "totals": {
                "projects": ProjectRepository.count_all(),
                "sprints": SprintRepository.count_all(),
                "issues": IssueRepository.count_all(),
                "users": UserRepository.count_all(),
            },
            "users": users,
        },
    }


@router.get("/users")
def get_users(
    search: str | None = Query(None),
    role: str | None = Query(None),
    current_user=Depends(require_admin),
):
    users = []

    for user in UserRepository.find_all(
        search=search,
        role=role,
    ):
        users.append(
            {
                "id": str(user["_id"]),
                "name": user["name"],
                "email": user["email"],
                "role": user["role"],
                "created_at": user.get("created_at"),
                "updated_at": user.get("updated_at"),
            }
        )

    return {
        "success": True,
        "message": "Users retrieved successfully",
        "data": {
            "users": users,
        },
    }


@router.put("/users/{user_id}")
def update_user(
    user_id: str,
    request: UpdateUserRequest,
    current_user=Depends(require_admin),
):
    user = UserRepository.find_by_id(user_id)

    if not user:
        raise UserNotFoundException()

    existing_user = UserRepository.find_by_email(request.email)

    if existing_user and str(existing_user["_id"]) != user_id:
        raise UserAlreadyExistsException()

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

    return {
        "success": True,
        "message": "User updated successfully",
        "data": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "created_at": user.get("created_at"),
            "updated_at": user.get("updated_at"),
        },
    }
