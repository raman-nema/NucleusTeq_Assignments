import uuid
from app.common.enums import Role
from app.core.database import database

# Helper Methods

def register_user(
    client,
    name,
    email,
    password,
    role,
):
    """Register a user."""

    client.post(
        "/auth/register",
        json={
            "name": name,
            "email": email,
            "password": password,
            "role": role,
        },
    )


def login_user(
    client,
    email,
    password,
):
    """Login and return access token."""

    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    return response.json()["data"]["access_token"]


def get_user_id(email):
    """Return MongoDB user id."""

    user = database.users.find_one(
        {
            "email": email,
        }
    )

    return str(user["_id"])


def create_project(
    client,
    token,
):
    """Create a project."""

    response = client.post(
        "/projects",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "name": f"Project-{uuid.uuid4()}",
            "description": "Project Description",
        },
    )

    return response.json()["data"]["id"]


def create_sprint(
    client,
    token,
    project_id,
):
    """Create sprint."""

    response = client.post(
        f"/projects/{project_id}/sprints",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "name": f"Sprint-{uuid.uuid4()}",
            "goal": "Sprint Goal",
            "start_date": "2026-07-01",
            "end_date": "2026-07-15",
            "status": "PLANNED",
        },
    )

    return response.json()["data"]["id"]

# Test Cases
def test_admin_can_create_issue(client):

    register_user(
        client,
        "Admin",
        "admin@company.com",
        "Admin@123",
        Role.ADMIN.value,
    )

    token = login_user(
        client,
        "admin@company.com",
        "Admin@123",
    )

    project_id = create_project(
        client,
        token,
    )

    sprint_id = create_sprint(
        client,
        token,
        project_id,
    )

    response = client.post(
        f"/projects/{project_id}/issues",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "Login Bug",
            "description": "Unable to login from homepage.",
            "assignee": get_user_id("admin@company.com"),
            "sprint_id": sprint_id,
            "priority": "HIGH",
            "status": "TODO",
        },
    )

    assert response.status_code == 403

def test_member_can_create_issue(client):

    register_user(
        client,
        "Admin",
        "admin@company.com",
        "Admin@123",
        Role.ADMIN.value,
    )

    register_user(
        client,
        "Member",
        "member@company.com",
        "Member@123",
        Role.MEMBER.value,
    )

    admin_token = login_user(
        client,
        "admin@company.com",
        "Admin@123",
    )

    member_token = login_user(
        client,
        "member@company.com",
        "Member@123",
    )

    member_id = get_user_id(
        "member@company.com",
    )

    project_id = create_project(
        client,
        admin_token,
    )

    client.post(
        f"/projects/{project_id}/members",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
        json={
            "user_id": member_id,
        },
    )

    sprint_id = create_sprint(
        client,
        admin_token,
        project_id,
    )

    response = client.post(
        f"/projects/{project_id}/issues",
        headers={
            "Authorization": f"Bearer {member_token}",
        },
        json={
            "title": "Profile Bug",
            "description": "Profile page is not loading.",
            "assignee": member_id,
            "sprint_id": sprint_id,
            "priority": "MEDIUM",
            "status": "TODO",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["type"] == "TASK"


def test_member_can_create_supported_issue_type(client):

    register_user(
        client,
        "Admin",
        "admin@company.com",
        "Admin@123",
        Role.ADMIN.value,
    )

    register_user(
        client,
        "Member",
        "member@company.com",
        "Member@123",
        Role.MEMBER.value,
    )

    admin_token = login_user(
        client,
        "admin@company.com",
        "Admin@123",
    )

    member_token = login_user(
        client,
        "member@company.com",
        "Member@123",
    )

    member_id = get_user_id(
        "member@company.com",
    )

    project_id = create_project(
        client,
        admin_token,
    )

    client.post(
        f"/projects/{project_id}/members",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
        json={
            "user_id": member_id,
        },
    )

    sprint_id = create_sprint(
        client,
        admin_token,
        project_id,
    )

    response = client.post(
        f"/projects/{project_id}/issues",
        headers={
            "Authorization": f"Bearer {member_token}",
        },
        json={
            "title": "Checkout Story",
            "description": "Customer can complete checkout.",
            "assignee": member_id,
            "sprint_id": sprint_id,
            "priority": "MEDIUM",
            "type": "STORY",
            "status": "TODO",
        },
    )

    assert response.status_code == 200
    assert response.json()["data"]["type"] == "STORY"


def test_member_cannot_create_unsupported_issue_type(client):

    register_user(
        client,
        "Admin",
        "admin@company.com",
        "Admin@123",
        Role.ADMIN.value,
    )

    register_user(
        client,
        "Member",
        "member@company.com",
        "Member@123",
        Role.MEMBER.value,
    )

    admin_token = login_user(
        client,
        "admin@company.com",
        "Admin@123",
    )

    member_token = login_user(
        client,
        "member@company.com",
        "Member@123",
    )

    member_id = get_user_id(
        "member@company.com",
    )

    project_id = create_project(
        client,
        admin_token,
    )

    client.post(
        f"/projects/{project_id}/members",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
        json={
            "user_id": member_id,
        },
    )

    sprint_id = create_sprint(
        client,
        admin_token,
        project_id,
    )

    response = client.post(
        f"/projects/{project_id}/issues",
        headers={
            "Authorization": f"Bearer {member_token}",
        },
        json={
            "title": "Unsupported Issue",
            "description": "Issue type should be rejected.",
            "assignee": member_id,
            "sprint_id": sprint_id,
            "priority": "MEDIUM",
            "type": "EPIC",
            "status": "TODO",
        },
    )

    assert response.status_code == 422


def test_viewer_cannot_create_issue(client):

    register_user(
        client,
        "Viewer",
        "viewer@company.com",
        "Viewer@123",
        Role.VIEWER.value,
    )

    token = login_user(
        client,
        "viewer@company.com",
        "Viewer@123",
    )

    response = client.post(
        "/projects/6855dca93a683df1a1111111/issues",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "Issue",
            "description": "Issue Description",
            "assignee": "6855dca93a683df1a1111112",
            "sprint_id": "6855dca93a683df1a1111113",
            "priority": "LOW",
            "status": "TODO",
        },
    )

    assert response.status_code == 403


def test_create_issue_without_token(client):

    response = client.post(
        "/projects/6855dca93a683df1a1111111/issues",
        json={
            "title": "Issue",
            "description": "Issue Description",
            "assignee": "6855dca93a683df1a1111112",
            "sprint_id": "6855dca93a683df1a1111113",
            "priority": "HIGH",
            "status": "TODO",
        },
    )

    assert response.status_code == 401


def test_create_issue_invalid_token(client):

    response = client.post(
        "/projects/6855dca93a683df1a1111111/issues",
        headers={
            "Authorization": "Bearer invalid-token",
        },
        json={
            "title": "Issue",
            "description": "Issue Description",
            "assignee": "6855dca93a683df1a1111112",
            "sprint_id": "6855dca93a683df1a1111113",
            "priority": "HIGH",
            "status": "TODO",
        },
    )

    assert response.status_code == 401


def test_create_issue_project_not_found(client):

    register_user(
        client,
        "Admin",
        "admin@company.com",
        "Admin@123",
        Role.ADMIN.value,
    )

    token = login_user(
        client,
        "admin@company.com",
        "Admin@123",
    )

    response = client.post(
        "/projects/6855dca93a683df1a1111111/issues",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "Issue",
            "description": "Issue Description",
            "assignee": "6855dca93a683df1a1111112",
            "sprint_id": "6855dca93a683df1a1111113",
            "priority": "HIGH",
            "status": "TODO",
        },
    )

    assert response.status_code == 404
