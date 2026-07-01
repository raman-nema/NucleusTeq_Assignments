from datetime import datetime
from bson import ObjectId
from app.common.enums import Role
from app.models.project_model import ProjectModel
from app.repositories.project_repository import ProjectRepository
from app.repositories.user_repository import UserRepository
from app.schemas.requests.project_member_request import (
    AssignMemberRequest,
)
from app.schemas.responses.project_response import (
    ProjectResponse,
    ProjectListResponse,
    DeleteProjectResponse,
    ProjectMemberResponse,
)
from app.exceptions.custom_exceptions import (
    ForbiddenException,
    ProjectAlreadyExistsException,
    ProjectNotFoundException,
    UserNotFoundException,
    MemberAlreadyAssignedException,
    MemberNotAssignedException,
)

class ProjectService:
    """Handles project-related business logic."""

    @staticmethod
    def create_project(request, current_user):

        # Check whether a project already exists with the same name.
        existing_project = ProjectRepository.find_by_name(request.name)

        if existing_project:
            raise ProjectAlreadyExistsException()

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
            members=[str(member) for member in project["members"]],
            created_at=project["created_at"],
            updated_at=project["updated_at"],
        )
    
    @staticmethod
    def get_all_projects(current_user):
        """Retrieve projects based on user role."""

        if current_user["role"] == Role.ADMIN.value or current_user["role"] == Role.VIEWER.value:
            projects = ProjectRepository.find_all()
        else:
            projects = ProjectRepository.find_by_member(
                str(current_user["_id"])
            )

        project_list = []

        for project in projects:

           project_list.append(
                ProjectResponse(
                    id=str(project["_id"]),
                    name=project["name"],
                    description=project["description"],
                    created_by=project["created_by"],
                    members=[
                        str(member)
                        for member in project.get("members", [])
                    ],
                    created_at=project["created_at"],
                    updated_at=project["updated_at"],
                )
            )

        return ProjectListResponse(
            projects=project_list,
        )
    @staticmethod
    def get_project_by_id(
        project_id: str,
        current_user,
    ):
        """Retrieve a project by its ID."""

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
        
        return ProjectResponse(
            id=str(project["_id"]),
            name=project["name"],
            description=project["description"],
            created_by=project["created_by"],
            members=[
                    str(member)
                    for member in project.get("members", [])
             ],
            created_at=project["created_at"],
            updated_at=project["updated_at"],
        )
    
    @staticmethod
    def update_project(
        project_id: str,
        request,
        current_user,
    ):

        project = ProjectRepository.find_by_id(project_id)

        if not project:
            raise ProjectNotFoundException()

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
            members=[
                str(member)
                for member in project.get("members", [])
            ],
            created_at=project["created_at"],
            updated_at=project["updated_at"],
        )   

    @staticmethod
    def delete_project(project_id: str):

        project = ProjectRepository.find_by_id(project_id)

        if not project:
            raise ProjectNotFoundException()

        ProjectRepository.delete_project(project_id)

        return DeleteProjectResponse(message="Project deleted successfully")

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

        if user["role"] != "MEMBER":
            raise ForbiddenException()

        members = project.get("members", [])

        if ObjectId(request.user_id) in members:
            raise MemberAlreadyAssignedException()

        ProjectRepository.add_member(
            project_id,
            request.user_id,
        )

        return ProjectMemberResponse(
            message="Member assigned successfully",
        )

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

        members = project.get("members", [])

        if ObjectId(user_id) not in members:
            raise MemberNotAssignedException()

        ProjectRepository.remove_member(
            project_id,
            user_id,
        )

        return ProjectMemberResponse(
            message="Member removed successfully",
        )