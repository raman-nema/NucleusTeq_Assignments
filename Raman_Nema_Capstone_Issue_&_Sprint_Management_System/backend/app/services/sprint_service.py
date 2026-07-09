from datetime import datetime, time
from app.common.enums import Role
from app.common.pagination import (
    apply_pagination,
    build_pagination_meta,
)
from app.models.sprint_model import SprintModel
from app.repositories.project_repository import ProjectRepository
from app.repositories.sprint_repository import SprintRepository
from app.schemas.requests.sprint_request import (
    CreateSprintRequest,
    UpdateSprintRequest,
)
from app.schemas.responses.sprint_response import (
    SprintResponse,
    SprintListResponse,
    DeleteSprintResponse,
)
from app.exceptions.custom_exceptions import (
    ForbiddenException,
    ProjectNotFoundException,
    SprintAlreadyExistsException,
    SprintNotFoundException,
)

class SprintService:
    """Handles sprint-related business logic."""

    @staticmethod
    def create_sprint(
        project_id: str,
        request: CreateSprintRequest,
        current_user: dict,
    ):
        """Create a new sprint."""

        project = ProjectRepository.find_by_id(project_id)
        if not project:
            raise ProjectNotFoundException()

        if current_user["role"] != Role.ADMIN.value and not ProjectRepository.is_member(
            project_id,
            str(current_user["_id"]),
        ):
            raise ForbiddenException()

        existing_sprint = SprintRepository.find_by_name(
            project_id,
            request.name,
        )

        if existing_sprint:
            raise SprintAlreadyExistsException()

        sprint = SprintModel.build(
            project_id=project_id,
            name=request.name,
            goal=request.goal,
            start_date=request.start_date,
            end_date=request.end_date,
            status=request.status,
            created_by=str(current_user["_id"]),
        )

        result = SprintRepository.create_sprint(sprint)

        return SprintResponse(
            id=str(result.inserted_id),
            project_id=str(sprint["project_id"]),
            name=sprint["name"],
            goal=sprint["goal"],
            start_date=sprint["start_date"],
            end_date=sprint["end_date"],
            status=sprint["status"],
            created_by=sprint["created_by"],
            created_at=sprint["created_at"],
            updated_at=sprint["updated_at"],
        )

    @staticmethod
    def get_all_sprints(project_id: str, current_user: dict, pagination):
        """Retrieve all sprints for a project."""

        project = ProjectRepository.find_by_id(project_id)

        if not project:
            raise ProjectNotFoundException()

        if current_user["role"] == Role.MEMBER.value:
            if not ProjectRepository.is_member(
                project_id,
                str(current_user["_id"]),
            ):
                raise ForbiddenException()

        total_sprints = SprintRepository.count_by_project(project_id)
        sprints = apply_pagination(
            SprintRepository.find_all_by_project(project_id),
            pagination,
        )

        sprint_list = []

        for sprint in sprints:
            sprint_list.append(
                SprintResponse(
                    id=str(sprint["_id"]),
                    project_id=str(sprint["project_id"]),
                    name=sprint["name"],
                    goal=sprint["goal"],
                    start_date=sprint["start_date"],
                    end_date=sprint["end_date"],
                    status=sprint["status"],
                    created_by=sprint["created_by"],
                    created_at=sprint["created_at"],
                    updated_at=sprint["updated_at"],
                )
            )

        return SprintListResponse(
            sprints=sprint_list,
            pagination=build_pagination_meta(
                total_sprints,
                pagination,
            ),
        )

    @staticmethod
    def get_sprint_by_id(sprint_id: str, current_user):
        """Retrieve a sprint by its ID."""

        sprint = SprintRepository.find_by_id(sprint_id)

        if not sprint:
            raise SprintNotFoundException()

        if current_user["role"] == Role.MEMBER.value:
            if not ProjectRepository.is_member(
                str(sprint["project_id"]),
                str(current_user["_id"]),
            ):
                raise ForbiddenException()

        return SprintResponse(
            id=str(sprint["_id"]),
            project_id=str(sprint["project_id"]),
            name=sprint["name"],
            goal=sprint["goal"],
            start_date=sprint["start_date"],
            end_date=sprint["end_date"],
            status=sprint["status"],
            created_by=sprint["created_by"],
            created_at=sprint["created_at"],
            updated_at=sprint["updated_at"],
        )

    @staticmethod
    def update_sprint(
        sprint_id: str,
        request: UpdateSprintRequest,
        current_user,
    ):
        """Update an existing sprint."""

        sprint = SprintRepository.find_by_id(sprint_id)
        if not sprint:
            raise SprintNotFoundException()

        if current_user["role"] != Role.ADMIN.value and not ProjectRepository.is_member(
            str(sprint["project_id"]),
            str(current_user["_id"]),
        ):
            raise ForbiddenException()

        existing_sprint = SprintRepository.find_by_name(
            str(sprint["project_id"]),
            request.name,
        )

        if existing_sprint and existing_sprint["_id"] != sprint["_id"]:
            raise SprintAlreadyExistsException()

        updated_data = {
            "name": request.name,
            "goal": request.goal,
            "start_date": datetime.combine(
                request.start_date,
                time.min,
            ),
            "end_date": datetime.combine(
                request.end_date,
                time.min,
            ),
            "status": request.status,
            "updated_at": datetime.utcnow(),
        }

        SprintRepository.update_sprint(
            sprint_id,
            updated_data,
        )

        sprint.update(updated_data)

        return SprintResponse(
            id=str(sprint["_id"]),
            project_id=str(sprint["project_id"]),
            name=sprint["name"],
            goal=sprint["goal"],
            start_date=sprint["start_date"],
            end_date=sprint["end_date"],
            status=sprint["status"],
            created_by=sprint["created_by"],
            created_at=sprint["created_at"],
            updated_at=sprint["updated_at"],
        )

    @staticmethod
    def delete_sprint(
        sprint_id: str,
        current_user,
    ):
        """Delete a sprint."""

        sprint = SprintRepository.find_by_id(sprint_id)

        if not sprint:
            raise SprintNotFoundException()

        if current_user["role"] != Role.ADMIN.value and not ProjectRepository.is_member(
            str(sprint["project_id"]),
            str(current_user["_id"]),
        ):
            raise ForbiddenException()

        SprintRepository.delete_sprint(sprint_id)

        return DeleteSprintResponse(
            message="Sprint deleted successfully",
        )
