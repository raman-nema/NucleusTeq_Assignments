from typing import Literal

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from app.common.api_response import ApiResponse
from app.common.pagination import get_pagination_params
from app.constants.message_constants import (
    COMMENT_ADDED_MESSAGE,
    COMMENT_DELETED_MESSAGE,
    COMMENT_UPDATED_MESSAGE,
    ISSUE_CREATED_MESSAGE,
    ISSUE_LIST_MESSAGE,
    ISSUE_RETRIEVED_MESSAGE,
    ISSUE_UPDATED_MESSAGE,
)
from app.dependencies.authentication import get_current_user
from app.dependencies.authorization import (
    require_admin_or_member,
)
from app.schemas.requests.issue_request import (
    CreateIssueCommentRequest,
    CreateIssueRequest,
    UpdateIssueCommentRequest,
    UpdateIssueRequest,
)
from app.services.issue_service import IssueService

router = APIRouter(
    tags=["Issues"],
)


@router.post("/projects/{project_id}/issues", response_model=ApiResponse)
def create_issue(
    project_id: str,
    request: CreateIssueRequest,
    current_user=Depends(require_admin_or_member),
):
    """Create an issue for a project."""

    response = IssueService.create_issue(
        project_id,
        request,
        current_user,
    )

    return ApiResponse(
        success=True,
        message=ISSUE_CREATED_MESSAGE,
        data=response.model_dump(),
    )


@router.get("/projects/{project_id}/issues", response_model=ApiResponse)
def get_all_issues(
    project_id: str,
    issue_status: Literal["TODO", "IN_PROGRESS", "DONE"] | None = Query(
        None,
        alias="status",
    ),
    assignee: str | None = Query(
        None,
        pattern=r"^[0-9a-fA-F]{24}$",
    ),
    pagination=Depends(get_pagination_params),
    current_user=Depends(get_current_user),
):
    """Retrieve all issues for a project."""

    response = IssueService.get_all_issues(
        project_id,
        current_user,
        pagination,
        issue_status,
        assignee,
    )

    return ApiResponse(
        success=True,
        message=ISSUE_LIST_MESSAGE,
        data=response.model_dump(),
    )


@router.get("/issues/{issue_id}", response_model=ApiResponse)
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
        message=ISSUE_RETRIEVED_MESSAGE,
        data=response.model_dump(),
    )

@router.post("/issues/{issue_id}/comments", response_model=ApiResponse)
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
        message=COMMENT_ADDED_MESSAGE,
        data=response.model_dump(),
    )


@router.put("/issues/{issue_id}/comments/{comment_id}", response_model=ApiResponse)
def update_comment_on_issue(
    issue_id: str,
    comment_id: str,
    request: UpdateIssueCommentRequest,
    current_user=Depends(require_admin_or_member),
):
    """Update a comment on an issue."""

    response = IssueService.update_comment(
        issue_id,
        comment_id,
        request,
        current_user,
    )

    return ApiResponse(
        success=True,
        message=COMMENT_UPDATED_MESSAGE,
        data=response.model_dump(),
    )


@router.delete("/issues/{issue_id}/comments/{comment_id}", response_model=ApiResponse)
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
        message=COMMENT_DELETED_MESSAGE,
        data=response.model_dump(),
    )


@router.put("/issues/{issue_id}", response_model=ApiResponse)
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
        message=ISSUE_UPDATED_MESSAGE,
        data=response.model_dump(),
    )


@router.delete("/issues/{issue_id}", response_model=ApiResponse)
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
