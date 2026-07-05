from datetime import datetime
from app.common.enums import Role
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
    CreateIssueRequest,
    UpdateIssueRequest,
)
from app.schemas.responses.issue_response import (
    IssueResponse,
    IssueListResponse,
    DeleteIssueResponse,
)
from app.exceptions.custom_exceptions import (
    ForbiddenException,
    ProjectNotFoundException,
    SprintNotFoundException,
    IssueAlreadyExistsException,
    IssueNotFoundException,
    UserNotFoundException,
)

class IssueService:
    """Handles issue-related business logic."""

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
            raise IssueAlreadyExistsException()

        # Build the issue document.
        issue = IssueModel.build(
            project_id=project_id,
            sprint_id=request.sprint_id,
            title=request.title,
            description=request.description,
            priority=request.priority,
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
            status=issue["status"],
            assignee=issue["assignee"],
            reporter=issue["reporter"],
            created_at=issue["created_at"],
            updated_at=issue["updated_at"],
        )

    @staticmethod
    def get_all_issues(
        project_id: str,
        current_user: dict,
        pagination,
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

        total_issues = IssueRepository.count_by_project(project_id)
        issues = apply_pagination(
            IssueRepository.find_all_by_project(project_id),
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
                    status=issue["status"],
                    assignee=issue["assignee"],
                    reporter=issue["reporter"],
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
            raise IssueNotFoundException()

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
            status=issue["status"],
            assignee=issue["assignee"],
            reporter=issue["reporter"],
            created_at=issue["created_at"],
            updated_at=issue["updated_at"],
        )

    @staticmethod
    def update_issue(
        issue_id: str,
        request: UpdateIssueRequest,
        current_user,
    ):
        """Update an existing issue."""

        issue = IssueRepository.find_by_id(issue_id)

        if not issue:
            raise IssueNotFoundException()

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
            raise IssueAlreadyExistsException()

        updated_data = {
            "sprint_id": sprint["_id"],
            "title": request.title,
            "description": request.description,
            "priority": request.priority,
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
            status=issue["status"],
            assignee=issue["assignee"],
            reporter=issue["reporter"],
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
            raise IssueNotFoundException()

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
