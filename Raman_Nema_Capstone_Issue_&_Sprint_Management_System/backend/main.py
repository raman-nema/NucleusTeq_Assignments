from fastapi import FastAPI
from app.routers.auth_router import router as auth_router
from app.routers import project_router
from app.routers import admin_router
from app.routers.sprint_router import router as sprint_router
from app.routers.issue_router import router as issue_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.seed import seed_admin
from app.exceptions.custom_exceptions import (
    UserAlreadyExistsException,
    InvalidCredentialsException,
    UnauthorizedException,
    ExpiredTokenException,
    ForbiddenException,
    ProjectAlreadyExistsException,
    ProjectHasSprintsException,
    ProjectNotFoundException,
    SprintAlreadyExistsException,
    SprintHasIssuesException,
    SprintNotFoundException,
    MemberAlreadyAssignedException,
    MemberNotAssignedException,
    UserNotFoundException,
    IssueAlreadyExistsException,
    IssueNotFoundException,
    InvalidIssueStatusTransitionException,
)
from app.exceptions.exception_handlers import (
    user_exists_handler,
    invalid_credentials_handler,
    unauthorized_handler,
    expired_token_handler,
    forbidden_handler,
    project_exists_handler,
    project_has_sprints_handler,
    project_not_found_handler,
    sprint_exists_handler,
    sprint_has_issues_handler,
    sprint_not_found_handler,
    member_already_assigned_handler,
    member_not_assigned_handler,
    user_not_found_handler,
    issue_exists_handler,
    issue_not_found_handler,
    invalid_issue_status_transition_handler,
)

app = FastAPI(title="Issue & Sprint Management System")

# Register authentication routes under the application.
app.include_router(auth_router)

app.include_router(admin_router.router)

app.include_router(project_router.router)

app.include_router(sprint_router)

app.include_router(issue_router)


# Map custom authentication exceptions to consistent JSON responses.
app.add_exception_handler(UserAlreadyExistsException, user_exists_handler)
app.add_exception_handler(InvalidCredentialsException, invalid_credentials_handler)
app.add_exception_handler(UnauthorizedException, unauthorized_handler)
app.add_exception_handler(ExpiredTokenException, expired_token_handler)
app.add_exception_handler(ForbiddenException, forbidden_handler)
app.add_exception_handler(ProjectAlreadyExistsException,project_exists_handler)
app.add_exception_handler(ProjectNotFoundException, project_not_found_handler)
app.add_exception_handler(ProjectHasSprintsException, project_has_sprints_handler)
app.add_exception_handler(SprintNotFoundException, sprint_not_found_handler)
app.add_exception_handler(SprintAlreadyExistsException, sprint_exists_handler)
app.add_exception_handler(SprintHasIssuesException, sprint_has_issues_handler)
app.add_exception_handler(MemberAlreadyAssignedException, member_already_assigned_handler)
app.add_exception_handler(MemberNotAssignedException, member_not_assigned_handler)
app.add_exception_handler(UserNotFoundException, user_not_found_handler)
app.add_exception_handler(IssueAlreadyExistsException, issue_exists_handler)
app.add_exception_handler(IssueNotFoundException, issue_not_found_handler)
app.add_exception_handler(
    InvalidIssueStatusTransitionException,
    invalid_issue_status_transition_handler,
)


# Allow the local frontend application to call the backend APIs.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    # Ensure the default admin user exists when the application starts.
    seed_admin()
    
