from datetime import datetime

from bson import ObjectId

from app.common.enums import Role
from app.common.pagination import apply_pagination, build_pagination_meta
from app.constants.message_constants import (
    PROJECT_ALREADY_EXISTS_MESSAGE,
    PROJECT_DELETED_MESSAGE,
    PROJECT_NOT_FOUND_MESSAGE,
)
from app.exceptions.custom_exceptions import (
    ConflictException,
    ForbiddenException,
    MemberAlreadyAssignedException,
    MemberNotAssignedException,
    NotFoundException,
    ProjectHasSprintsException,
    ProjectNotFoundException,
    UserNotFoundException,
)
from app.models.project_model import ProjectModel
from app.repositories.project_repository import ProjectRepository
from app.repositories.sprint_repository import SprintRepository
from app.repositories.user_repository import UserRepository
from app.schemas.requests.project_member_request import AssignMemberRequest
from app.schemas.responses.project_response import (
    DeleteProjectResponse,
    ProjectListResponse,
    ProjectMemberResponse,
    ProjectMemberSummary,
    ProjectResponse,
)


class ProjectService:
    """Handles project-related business logic."""

    @staticmethod
    def _build_member_summaries(member_ids):
        """Build member display details from stored user IDs."""

        members = []

        for member_id in member_ids:
            user = UserRepository.find_by_id(str(member_id))

            if user:
                members.append(
                    ProjectMemberSummary(
                        id=str(user["_id"]),
                        name=user["name"],
                        role=user["role"],
                    )
                )
            else:
                members.append(
                    ProjectMemberSummary(
                        id=str(member_id),
                        name="Unknown user",
                        role="UNKNOWN",
                    )
                )

        return members

    @staticmethod
    def _build_project_response(project):
        """Build a project response from a Mongo document."""

        return ProjectResponse(
            id=str(project["_id"]),
            name=project["name"],
            description=project["description"],
            created_by=project["created_by"],
            members=ProjectService._build_member_summaries(
                project.get("members", [])
            ),
            created_at=project["created_at"],
            updated_at=project["updated_at"],
        )

    @staticmethod
    def create_project(request, current_user):
        """Create a new project."""

        existing_project = ProjectRepository.find_by_name(request.name)

        if existing_project:
            raise ConflictException(PROJECT_ALREADY_EXISTS_MESSAGE)

        project = ProjectModel.build(
            name=request.name,
            description=request.description,
            created_by=str(current_user["_id"]),
        )

        result = ProjectRepository.create_project(project)
        project["_id"] = result.inserted_id

        return ProjectService._build_project_response(project)

    @staticmethod
    def get_all_projects(current_user, pagination):
        """Retrieve projects based on user role."""

        if current_user["role"] in (Role.ADMIN.value, Role.VIEWER.value):
            total_projects = ProjectRepository.count_all()
            projects = ProjectRepository.find_all(
                skip=pagination.skip,
                limit=pagination.limit,
            )
        else:
            total_projects = ProjectRepository.count_by_member(
                str(current_user["_id"])
            )
            projects = apply_pagination(
                ProjectRepository.find_by_member(str(current_user["_id"])),
                pagination,
            )

        return ProjectListResponse(
            projects=[
                ProjectService._build_project_response(project)
                for project in projects
            ],
            pagination=build_pagination_meta(total_projects, pagination),
        )

    @staticmethod
    def get_project_by_id(project_id: str, current_user):
        """Retrieve a project by its ID."""

        project = ProjectRepository.find_by_id(project_id)

        if not project:
            raise NotFoundException(PROJECT_NOT_FOUND_MESSAGE)

        if (
            current_user["role"] == Role.MEMBER.value
            and not ProjectRepository.is_member(
                project_id,
                str(current_user["_id"]),
            )
        ):
            raise ForbiddenException()

        return ProjectService._build_project_response(project)

    @staticmethod
    def update_project(project_id: str, request, current_user):
        """Update an existing project."""

        project = ProjectRepository.find_by_id(project_id)

        if not project:
            raise NotFoundException(PROJECT_NOT_FOUND_MESSAGE)

        if (
            current_user["role"] != Role.ADMIN.value
            and not ProjectRepository.is_member(
                project_id,
                str(current_user["_id"]),
            )
        ):
            raise ForbiddenException()

        updated_data = {
            "name": request.name,
            "description": request.description,
            "updated_at": datetime.utcnow(),
        }

        ProjectRepository.update_project(project_id, updated_data)
        project.update(updated_data)

        return ProjectService._build_project_response(project)

    @staticmethod
    def delete_project(project_id: str):
        """Delete a project."""

        project = ProjectRepository.find_by_id(project_id)

        if not project:
            raise NotFoundException(PROJECT_NOT_FOUND_MESSAGE)

        if SprintRepository.count_by_project(project_id) > 0:
            raise ProjectHasSprintsException()

        ProjectRepository.delete_project(project_id)

        return DeleteProjectResponse(message=PROJECT_DELETED_MESSAGE)

    @staticmethod
    def assign_member(
        project_id: str,
        request: AssignMemberRequest,
        current_user,
    ):
        """Assign a member to a project."""

        project = ProjectRepository.find_by_id(project_id)

        if not project:
            raise ProjectNotFoundException()

        user = UserRepository.find_by_id(request.user_id)

        if not user:
            raise UserNotFoundException()

        if user["role"] != Role.MEMBER.value:
            raise ForbiddenException()

        if ObjectId(request.user_id) in project.get("members", []):
            raise MemberAlreadyAssignedException()

        ProjectRepository.add_member(project_id, request.user_id)

        return ProjectMemberResponse(message="Member assigned successfully")

    @staticmethod
    def remove_member(
        project_id: str,
        user_id: str,
        current_user,
    ):
        """Remove a member from a project."""

        project = ProjectRepository.find_by_id(project_id)

        if not project:
            raise ProjectNotFoundException()

        user = UserRepository.find_by_id(user_id)

        if not user:
            raise UserNotFoundException()

        if ObjectId(user_id) not in project.get("members", []):
            raise MemberNotAssignedException()

        ProjectRepository.remove_member(project_id, user_id)

        return ProjectMemberResponse(message="Member removed successfully")
