from datetime import datetime, time
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
    def get_all_sprints(project_id: str):
        """Retrieve all sprints for a project."""

        project = ProjectRepository.find_by_id(project_id)

        if not project:
            raise ProjectNotFoundException()

        sprints = SprintRepository.find_all_by_project(project_id)

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
        )

    @staticmethod
    def get_sprint_by_id(sprint_id: str):
        """Retrieve a sprint by its ID."""

        sprint = SprintRepository.find_by_id(sprint_id)

        if not sprint:
            raise SprintNotFoundException()

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
    ):
        """Update an existing sprint."""

        sprint = SprintRepository.find_by_id(sprint_id)

        if not sprint:
            raise SprintNotFoundException()

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
    def delete_sprint(sprint_id: str):
        """Delete a sprint."""

        sprint = SprintRepository.find_by_id(sprint_id)

        if not sprint:
            raise SprintNotFoundException()

        SprintRepository.delete_sprint(sprint_id)

        return DeleteSprintResponse(
            message="Sprint deleted successfully",
        )
