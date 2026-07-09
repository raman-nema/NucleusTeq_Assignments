from fastapi import APIRouter
from fastapi import Depends
from app.common.api_response import ApiResponse
from app.common.pagination import PaginationParams, get_pagination_params
from app.constants.message_constants import (
    PROJECT_CREATED_MESSAGE,
    PROJECT_LIST_MESSAGE,
    PROJECT_RETRIEVED_MESSAGE,
    PROJECT_UPDATED_MESSAGE,
)
from app.services.project_service import ProjectService
from app.schemas.requests.project_request import (
    CreateProjectRequest,
    UpdateProjectRequest,
)
from app.dependencies.authentication import get_current_user
from app.dependencies.authorization import (
    require_admin,
    require_admin_or_member,
)
from app.services.sprint_service import SprintService
from app.schemas.requests.sprint_request import CreateSprintRequest
from app.schemas.requests.project_member_request import (
    AssignMemberRequest,
)

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.post("", response_model=ApiResponse)
def create_project(
    request: CreateProjectRequest,
    current_user=Depends(require_admin),
):
    """Create a new project."""

    response = ProjectService.create_project(
        request,
        current_user,
    )

    return ApiResponse(
        success=True,
        message=PROJECT_CREATED_MESSAGE,
        data=response.model_dump(),
    )


@router.get("", response_model=ApiResponse)
def get_all_projects(
    pagination: PaginationParams = Depends(get_pagination_params),
    current_user=Depends(get_current_user),
):
    """Retrieve all projects."""


    response = ProjectService.get_all_projects(pagination)

    return ApiResponse(
        success=True,
        message=PROJECT_LIST_MESSAGE,
        data=response.model_dump(),
    )


@router.get("/{project_id}", response_model=ApiResponse)
def get_project_by_id(
    project_id: str,
    current_user=Depends(get_current_user),
):
    """Retrieve a project by its ID."""

    response = ProjectService.get_project_by_id(
        project_id,
        current_user,
    )

    return ApiResponse(
        success=True,
        message=PROJECT_RETRIEVED_MESSAGE,
        data=response.model_dump(),
    )


@router.put("/{project_id}", response_model=ApiResponse)
def update_project(
    project_id: str,
    request: UpdateProjectRequest,
    current_user=Depends(require_admin_or_member),
):
    """Update an existing project."""

    response = ProjectService.update_project(
        project_id,
        request,
        current_user,
    )

    return ApiResponse(
        success=True,
        message=PROJECT_UPDATED_MESSAGE,
        data=response.model_dump(),
    )


@router.delete("/{project_id}", response_model=ApiResponse)
def delete_project(
    project_id: str,
    current_user=Depends(require_admin),
):
    """Delete an existing project."""

    response = ProjectService.delete_project(
        project_id,
    )

    return ApiResponse(
        success=True,
        message=response.message,
        data=None,
    )


@router.post("/{project_id}/members", response_model=ApiResponse)
def assign_member(
    project_id: str,
    request: AssignMemberRequest,
    current_user=Depends(require_admin),
):
    """Assign a member to a project."""

    response = ProjectService.assign_member(
        project_id,
        request,
        current_user,
    )

    return ApiResponse(
        success=True,
        message=response.message,
        data=None,
    )


@router.delete("/{project_id}/members/{user_id}", response_model=ApiResponse)
def remove_member(
    project_id: str,
    user_id: str,
    current_user=Depends(require_admin),
):
    """Remove a member from a project."""

    response = ProjectService.remove_member(
        project_id,
        user_id,
        current_user,
    )

    return ApiResponse(
        success=True,
        message=response.message,
        data=None,
    )


# Sprint routes for a specific project.
@router.post("/{project_id}/sprints", response_model=ApiResponse)
def create_sprint(
    project_id: str,
    request: CreateSprintRequest,
    current_user=Depends(require_admin_or_member),
):
    """Create a sprint for a project."""

    response = SprintService.create_sprint(
        project_id,
        request,
        current_user,
    )

    return ApiResponse(
        success=True,
        message="Sprint created successfully",
        data=response.model_dump(),
    )


@router.get("/{project_id}/sprints", response_model=ApiResponse)
def get_all_sprints(
    project_id: str,
    current_user=Depends(get_current_user),
):
    """Retrieve all sprints for a project."""

    response = SprintService.get_all_sprints(
        project_id,
        current_user,
    )

    return ApiResponse(
        success=True,
        message="Sprints retrieved successfully",
        data=response.model_dump(),
    )
