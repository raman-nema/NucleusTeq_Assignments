from datetime import datetime
from app.common.pagination import build_pagination_meta
from app.constants.message_constants import (
    PROJECT_ALREADY_EXISTS_MESSAGE,
    PROJECT_DELETED_MESSAGE,
    PROJECT_NOT_FOUND_MESSAGE,
)
from app.models.project_model import ProjectModel
from app.repositories.project_repository import ProjectRepository
from app.schemas.responses.project_response import (
    ProjectResponse,
    ProjectListResponse,
    DeleteProjectResponse,
)
from app.exceptions.custom_exceptions import (
    ConflictException,
    NotFoundException,
)


class ProjectService:
    """Handles project-related business logic."""

    @staticmethod
    def create_project(request, current_user):

        # Check whether a project already exists with the same name.
        existing_project = ProjectRepository.find_by_name(request.name)

        if existing_project:
            raise ConflictException(PROJECT_ALREADY_EXISTS_MESSAGE)

        # Build the project document.
        project = ProjectModel.build(
            name=request.name,
            description=request.description,
            created_by=str(current_user["_id"]),
        )

        # Save the project.
        result = ProjectRepository.create_project(project)

        return ProjectResponse(
            id=str(result.inserted_id),
            name=project["name"],
            description=project["description"],
            created_by=project["created_by"],
            created_at=project["created_at"],
            updated_at=project["updated_at"],
        )

    @staticmethod
    def get_all_projects(pagination):

        total_projects = ProjectRepository.count_all()
        projects = ProjectRepository.find_all(
            skip=pagination.skip,
            limit=pagination.limit,
        )

        project_list = []

        for project in projects:

            project_list.append(
                ProjectResponse(
                    id=str(project["_id"]),
                    name=project["name"],
                    description=project["description"],
                    created_by=project["created_by"],
                    created_at=project["created_at"],
                    updated_at=project["updated_at"],
                )
            )

        return ProjectListResponse(
            projects=project_list,
            pagination=build_pagination_meta(total_projects, pagination),
        )

    @staticmethod
    def get_project_by_id(project_id: str):

        project = ProjectRepository.find_by_id(project_id)

        if not project:
            raise NotFoundException(PROJECT_NOT_FOUND_MESSAGE)

        return ProjectResponse(
            id=str(project["_id"]),
            name=project["name"],
            description=project["description"],
            created_by=project["created_by"],
            created_at=project["created_at"],
            updated_at=project["updated_at"],
        )

    @staticmethod
    def update_project(project_id: str, request):

        project = ProjectRepository.find_by_id(project_id)

        if not project:
            raise NotFoundException(PROJECT_NOT_FOUND_MESSAGE)

        updated_data = {
            "name": request.name,
            "description": request.description,
            "updated_at": datetime.utcnow(),
        }

        ProjectRepository.update_project(
            project_id,
            updated_data,
        )

        project.update(updated_data)

        return ProjectResponse(
            id=str(project["_id"]),
            name=project["name"],
            description=project["description"],
            created_by=project["created_by"],
            created_at=project["created_at"],
            updated_at=project["updated_at"],
        )

    @staticmethod
    def delete_project(project_id: str):

        project = ProjectRepository.find_by_id(project_id)

        if not project:
            raise NotFoundException(PROJECT_NOT_FOUND_MESSAGE)

        ProjectRepository.delete_project(project_id)

        return DeleteProjectResponse(message=PROJECT_DELETED_MESSAGE)
