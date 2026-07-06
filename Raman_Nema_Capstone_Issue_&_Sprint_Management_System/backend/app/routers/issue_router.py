from fastapi import APIRouter
from fastapi import Depends

from app.common.api_response import ApiResponse
from app.dependencies.authentication import get_current_user
from app.dependencies.authorization import (
    require_admin_or_member,
)
from app.schemas.requests.issue_request import (
    CreateIssueCommentRequest,
    CreateIssueRequest,
    UpdateIssueRequest,
)
from app.services.issue_service import IssueService

router = APIRouter(
    prefix="/issues",
    tags=["Issues"],
)

@router.get("/{issue_id}", response_model=ApiResponse)
def get_issue_by_id(
    issue_id: str,
    current_user=Depends(get_current_user),
):
    """Retrieve an issue by its ID."""

    response = IssueService.get_issue_by_id(
        issue_id,
        current_user,
    )

    return ApiResponse(
        success=True,
        message="Issue retrieved successfully",
        data=response.model_dump(),
    )

@router.post("/{issue_id}/comments", response_model=ApiResponse)
def add_comment_to_issue(
    issue_id: str,
    request: CreateIssueCommentRequest,
    current_user=Depends(require_admin_or_member),
):
    """Add a comment to an existing issue."""

    response = IssueService.add_comment(
        issue_id,
        request,
        current_user,
    )

    return ApiResponse(
        success=True,
        message="Comment added successfully",
        data=response.model_dump(),
    )


@router.delete("/{issue_id}/comments/{comment_id}", response_model=ApiResponse)
def delete_comment_from_issue(
    issue_id: str,
    comment_id: str,
    current_user=Depends(require_admin_or_member),
):
    """Delete a comment from an issue."""

    response = IssueService.delete_comment(
        issue_id,
        comment_id,
        current_user,
    )

    return ApiResponse(
        success=True,
        message="Comment deleted successfully",
        data=response.model_dump(),
    )


@router.put("/{issue_id}", response_model=ApiResponse)
def update_issue(
    issue_id: str,
    request: UpdateIssueRequest,
    current_user=Depends(require_admin_or_member),
):
    """Update an existing issue."""

    response = IssueService.update_issue(
        issue_id,
        request,
        current_user,
    )

    return ApiResponse(
        success=True,
        message="Issue updated successfully",
        data=response.model_dump(),
    )

@router.delete("/{issue_id}", response_model=ApiResponse)
def delete_issue(
    issue_id: str,
    current_user=Depends(require_admin_or_member),
):
    """Delete an existing issue."""

    response = IssueService.delete_issue(
        issue_id,
        current_user,
    )

    return ApiResponse(
        success=True,
        message=response.message,
        data=None,
    )
