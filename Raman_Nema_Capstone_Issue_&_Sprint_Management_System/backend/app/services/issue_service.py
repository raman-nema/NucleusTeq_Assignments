from datetime import datetime

from bson import ObjectId
from fastapi import HTTPException
from fastapi import status

from app.common.enums import Role
from app.common.messages import (
    INVALID_ISSUE_STATUS_TRANSITION,
    ISSUE_ALREADY_EXISTS,
    ISSUE_NOT_FOUND,
)
from app.common.pagination import (
    apply_pagination,
    build_pagination_meta,
)
from app.models.issue_model import IssueModel
from app.repositories.project_repository import ProjectRepository
from app.repositories.sprint_repository import SprintRepository
from app.repositories.issue_repository import IssueRepository
from app.repositories.user_repository import UserRepository
from app.schemas.requests.issue_request import (
    CreateIssueCommentRequest,
    CreateIssueRequest,
    UpdateIssueCommentRequest,
    UpdateIssueRequest,
)
from app.schemas.responses.issue_response import (
    IssueCommentResponse,
    IssueResponse,
    IssueListResponse,
    DeleteIssueResponse,
)
from app.exceptions.custom_exceptions import (
    ForbiddenException,
    IssueNotFoundException,
    ProjectNotFoundException,
    SprintNotFoundException,
    UserNotFoundException,
)


class IssueService:
    """Handles issue-related business logic."""

    @staticmethod
    def _serialize_comments(comments: list | None):
        """Convert stored comment documents into response objects."""

        return [
            IssueCommentResponse(
                id=str(comment.get("_id")) if comment.get("_id") else None,
                user_id=str(comment["user_id"]),
                user_name=comment.get("user_name", "Unknown"),
                text=comment["text"],
                created_at=comment["created_at"],
            )
            for comment in comments or []
        ]

    @staticmethod
    def _build_issue_response(issue: dict):
        """Build an issue response from a Mongo document."""

        return IssueResponse(
            id=str(issue["_id"]),
            project_id=str(issue["project_id"]),
            sprint_id=str(issue["sprint_id"]),
            title=issue["title"],
            description=issue["description"],
            priority=issue["priority"],
            type=issue.get("type", "TASK"),
            status=issue["status"],
            assignee=issue["assignee"],
            reporter=issue["reporter"],
            comments=IssueService._serialize_comments(issue.get("comments", [])),
            created_at=issue["created_at"],
            updated_at=issue["updated_at"],
        )

    @staticmethod
    def _get_comment(issue: dict, comment_id: str):
        """Find a comment embedded in an issue."""

        for comment in issue.get("comments", []):
            if str(comment.get("_id")) == comment_id:
                return comment

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    @staticmethod
    def _ensure_comment_modifier(issue: dict, comment: dict, current_user: dict):
        """Allow admins or the original comment author to modify a comment."""

        if current_user["role"] == Role.ADMIN.value:
            return

        if not ProjectRepository.is_member(
            str(issue["project_id"]),
            str(current_user["_id"]),
        ):
            raise ForbiddenException()

        if str(comment["user_id"]) != str(current_user["_id"]):
            raise ForbiddenException()

    @staticmethod
    def create_issue(
        project_id: str,
        request: CreateIssueRequest,
        current_user: dict,
    ):
        """Create a new issue."""

        # Verify that the project exists.
        project = ProjectRepository.find_by_id(project_id)

        if not project:
            raise ProjectNotFoundException()

        # Verify that the sprint exists.
        sprint = SprintRepository.find_by_id(request.sprint_id)

        if not sprint:
            raise SprintNotFoundException()

        # Ensure the sprint belongs to the given project.
        if str(sprint["project_id"]) != project_id:
            raise ForbiddenException()

        # Only admins or members assigned to the project can create issues.
        if (
            current_user["role"] != Role.ADMIN.value
            and not ProjectRepository.is_member(
                project_id,
                str(current_user["_id"]),
            )
        ):
            raise ForbiddenException()

        # Verify that the assignee exists.
        assignee = UserRepository.find_by_id(request.assignee)

        if not assignee:
            raise UserNotFoundException()

        # Only members can be assigned issues.
        if assignee["role"] != Role.MEMBER.value:
            raise ForbiddenException()

        # Ensure the assignee belongs to the project.
        if not ProjectRepository.is_member(
            project_id,
            request.assignee,
        ):
            raise ForbiddenException()

        # Prevent duplicate issue titles within the same project.
        existing_issue = IssueRepository.find_by_title(
            project_id,
            request.title,
        )

        if existing_issue:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=ISSUE_ALREADY_EXISTS,
            )

        # Build the issue document.
        issue = IssueModel.build(
            project_id=project_id,
            sprint_id=request.sprint_id,
            title=request.title,
            description=request.description,
            priority=request.priority,
            type=request.type,
            status=request.status,
            assignee=request.assignee,
            reporter=str(current_user["_id"]),
        )

        # Save the issue.
        result = IssueRepository.create_issue(issue)

        return IssueResponse(
            id=str(result.inserted_id),
            project_id=str(issue["project_id"]),
            sprint_id=str(issue["sprint_id"]),
            title=issue["title"],
            description=issue["description"],
            priority=issue["priority"],
            type=issue["type"],
            status=issue["status"],
            assignee=issue["assignee"],
            reporter=issue["reporter"],
            comments=IssueService._serialize_comments(issue.get("comments", [])),
            created_at=issue["created_at"],
            updated_at=issue["updated_at"],
        )

    @staticmethod
    def get_all_issues(
        project_id: str,
        current_user: dict,
        pagination,
        status: str | None = None,
    ):
        """Retrieve all issues for a project."""

        project = ProjectRepository.find_by_id(project_id)

        if not project:
            raise ProjectNotFoundException()

        if (
            current_user["role"] == Role.MEMBER.value
            and not ProjectRepository.is_member(
                project_id,
                str(current_user["_id"]),
            )
        ):
            raise ForbiddenException()

        total_issues = IssueRepository.count_by_project(
            project_id,
            status,
        )
        issues = apply_pagination(
            IssueRepository.find_all_by_project(
                project_id,
                status,
            ),
            pagination,
        )

        issue_list = []

        for issue in issues:
            issue_list.append(
                IssueResponse(
                    id=str(issue["_id"]),
                    project_id=str(issue["project_id"]),
                    sprint_id=str(issue["sprint_id"]),
                    title=issue["title"],
                    description=issue["description"],
                    priority=issue["priority"],
                    type=issue.get("type", "TASK"),
                    status=issue["status"],
                    assignee=issue["assignee"],
                    reporter=issue["reporter"],
                    comments=IssueService._serialize_comments(issue.get("comments", [])),
                    created_at=issue["created_at"],
                    updated_at=issue["updated_at"],
                )
            )

        return IssueListResponse(
            issues=issue_list,
            pagination=build_pagination_meta(
                total_issues,
                pagination,
            ),
        )

    @staticmethod
    def get_issue_by_id(
        issue_id: str,
        current_user,
    ):
        """Retrieve an issue by its ID."""

        issue = IssueRepository.find_by_id(issue_id)

        if not issue:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ISSUE_NOT_FOUND,
            )

        if (
            current_user["role"] == Role.MEMBER.value
            and not ProjectRepository.is_member(
                str(issue["project_id"]),
                str(current_user["_id"]),
            )
        ):
            raise ForbiddenException()

        return IssueResponse(
            id=str(issue["_id"]),
            project_id=str(issue["project_id"]),
            sprint_id=str(issue["sprint_id"]),
            title=issue["title"],
            description=issue["description"],
            priority=issue["priority"],
            type=issue.get("type", "TASK"),
            status=issue["status"],
            assignee=issue["assignee"],
            reporter=issue["reporter"],
            comments=IssueService._serialize_comments(issue.get("comments", [])),
            created_at=issue["created_at"],
            updated_at=issue["updated_at"],
        )

    @staticmethod
    def add_comment(
        issue_id: str,
        request: CreateIssueCommentRequest,
        current_user,
    ):
        """Add a comment to an issue."""

        issue = IssueRepository.find_by_id(issue_id)

        if not issue:
            raise IssueNotFoundException()

        if (
            current_user["role"] != Role.ADMIN.value
            and not ProjectRepository.is_member(
                str(issue["project_id"]),
                str(current_user["_id"]),
            )
        ):
            raise ForbiddenException()

        comment = {
            "_id": ObjectId(),
            "user_id": str(current_user["_id"]),
            "user_name": current_user.get("name", "Unknown"),
            "text": request.text,
            "created_at": datetime.utcnow(),
        }

        IssueRepository.add_comment(issue_id, comment)

        updated_issue = IssueRepository.find_by_id(issue_id)

        return IssueService._build_issue_response(updated_issue)

    @staticmethod
    def update_comment(
        issue_id: str,
        comment_id: str,
        request: UpdateIssueCommentRequest,
        current_user,
    ):
        """Update a comment on an issue."""

        issue = IssueRepository.find_by_id(issue_id)

        if not issue:
            raise IssueNotFoundException()

        comment = IssueService._get_comment(issue, comment_id)
        IssueService._ensure_comment_modifier(issue, comment, current_user)

        IssueRepository.update_comment(
            issue_id,
            comment_id,
            {
                "text": request.text,
                "updated_at": datetime.utcnow(),
            },
        )

        updated_issue = IssueRepository.find_by_id(issue_id)

        return IssueService._build_issue_response(updated_issue)

    @staticmethod
    def delete_comment(
        issue_id: str,
        comment_id: str,
        current_user,
    ):
        """Delete a comment from an issue."""

        issue = IssueRepository.find_by_id(issue_id)

        if not issue:
            raise IssueNotFoundException()

        comment = IssueService._get_comment(issue, comment_id)
        IssueService._ensure_comment_modifier(issue, comment, current_user)

        IssueRepository.delete_comment(issue_id, comment_id)

        updated_issue = IssueRepository.find_by_id(issue_id)

        return IssueService._build_issue_response(updated_issue)

    @staticmethod
    def update_issue(
        issue_id: str,
        request: UpdateIssueRequest,
        current_user,
    ):
        """Update an existing issue."""

        issue = IssueRepository.find_by_id(issue_id)

        if not issue:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ISSUE_NOT_FOUND,
            )

        sprint = SprintRepository.find_by_id(
            request.sprint_id,
        )

        if not sprint:
            raise SprintNotFoundException()

        # Ensure the sprint belongs to the same project.
        if str(sprint["project_id"]) != str(issue["project_id"]):
            raise ForbiddenException()

        # Only admins or project members can update issues.
        if (
            current_user["role"] != Role.ADMIN.value
            and not ProjectRepository.is_member(
                str(issue["project_id"]),
                str(current_user["_id"]),
            )
        ):
            raise ForbiddenException()

        # Verify that the assignee exists.
        assignee = UserRepository.find_by_id(request.assignee)

        if not assignee:
            raise UserNotFoundException()

        # Only members can be assigned issues.
        if assignee["role"] != Role.MEMBER.value:
            raise ForbiddenException()

        # Ensure the assignee belongs to the project.
        if not ProjectRepository.is_member(
            str(issue["project_id"]),
            request.assignee,
        ):
            raise ForbiddenException()

        # Prevent duplicate issue titles within the same project.
        existing_issue = IssueRepository.find_by_title(
            str(issue["project_id"]),
            request.title,
        )

        if (
            existing_issue
            and existing_issue["_id"] != issue["_id"]
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=ISSUE_ALREADY_EXISTS,
            )

        if (
            current_user["role"] == Role.MEMBER.value
            and issue["status"] == "DONE"
            and request.status != "DONE"
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=INVALID_ISSUE_STATUS_TRANSITION,
            )

        updated_data = {
            "sprint_id": sprint["_id"],
            "title": request.title,
            "description": request.description,
            "priority": request.priority,
            "type": request.type,
            "status": request.status,
            "assignee": request.assignee,
            "updated_at": datetime.utcnow(),
        }

        IssueRepository.update_issue(
            issue_id,
            updated_data,
        )

        issue.update(updated_data)

        return IssueResponse(
            id=str(issue["_id"]),
            project_id=str(issue["project_id"]),
            sprint_id=str(issue["sprint_id"]),
            title=issue["title"],
            description=issue["description"],
            priority=issue["priority"],
            type=issue.get("type", "TASK"),
            status=issue["status"],
            assignee=issue["assignee"],
            reporter=issue["reporter"],
            comments=IssueService._serialize_comments(issue.get("comments", [])),
            created_at=issue["created_at"],
            updated_at=issue["updated_at"],
        )

    @staticmethod
    def delete_issue(
        issue_id: str,
        current_user,
    ):
        """Delete an issue."""

        issue = IssueRepository.find_by_id(issue_id)

        if not issue:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ISSUE_NOT_FOUND,
            )

        if (
            current_user["role"] != Role.ADMIN.value
            and not ProjectRepository.is_member(
                str(issue["project_id"]),
                str(current_user["_id"]),
            )
        ):
            raise ForbiddenException()

        IssueRepository.delete_issue(issue_id)

        return DeleteIssueResponse(
            message="Issue deleted successfully",
        )
