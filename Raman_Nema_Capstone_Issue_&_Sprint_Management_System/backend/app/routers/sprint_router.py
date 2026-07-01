from fastapi import APIRouter
from fastapi import Depends
from app.common.api_response import ApiResponse
from app.dependencies.authentication import get_current_user
from app.dependencies.authorization import (
    require_admin,
    require_admin_or_member,
)
from app.schemas.requests.sprint_request import UpdateSprintRequest
from app.services.sprint_service import SprintService

router = APIRouter(
    prefix="/sprints",
    tags=["Sprints"],
)

# Create and list sprint routes are defined in the Project router
# because sprints are nested resources of a project.

@router.get("/{sprint_id}", response_model=ApiResponse)
def get_sprint_by_id(
    sprint_id: str,
    current_user=Depends(get_current_user),
):
    """Retrieve a sprint by its ID."""

    response = SprintService.get_sprint_by_id(
        sprint_id,
    )

    return ApiResponse(
        success=True,
        message="Sprint retrieved successfully",
        data=response.model_dump(),
    )


@router.put("/{sprint_id}", response_model=ApiResponse)
def update_sprint(
    sprint_id: str,
    request: UpdateSprintRequest,
    current_user=Depends(require_admin_or_member),
):
    """Update an existing sprint."""

    response = SprintService.update_sprint(
        sprint_id,
        request,
    )

    return ApiResponse(
        success=True,
        message="Sprint updated successfully",
        data=response.model_dump(),
    )


@router.delete("/{sprint_id}", response_model=ApiResponse)
def delete_sprint(
    sprint_id: str,
    current_user=Depends(require_admin),
):
    """Delete an existing sprint."""

    response = SprintService.delete_sprint(
        sprint_id,
    )

    return ApiResponse(
        success=True,
        message=response.message,
        data=None,
    )