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
    """Login user and return access token."""

    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    return response.json()["data"]["access_token"]

def get_user_id(email):
    """Return user id."""

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
    """Create project."""

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

def create_issue(
    client,
    token,
    project_id,
    sprint_id,
    assignee_id,
):
    """Create issue."""

    response = client.post(
        f"/projects/{project_id}/issues",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": f"Issue-{uuid.uuid4()}",
            "description": "Issue Description",
            "assignee": assignee_id,
            "sprint_id": sprint_id,
            "priority": "HIGH",
            "status": "TODO",
        },
    )

    return response.json()["data"]["id"]


def test_admin_can_delete_issue(client):

    register_user(client, "Admin", "admin@company.com", "Admin@123", Role.ADMIN.value)
    register_user(client, "Member", "member@company.com", "Member@123", Role.MEMBER.value)

    admin_token = login_user(
        client,
        "admin@company.com",
        "Admin@123",
    )

    member_id = get_user_id("member@company.com")

    project_id = create_project(
        client,
        admin_token,
    )

    client.post(
        f"/projects/{project_id}/members",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"user_id": member_id},
    )

    sprint_id = create_sprint(
        client,
        admin_token,
        project_id,
    )

    issue_id = create_issue(
        client,
        admin_token,
        project_id,
        sprint_id,
        member_id,
    )

    response = client.delete(
        f"/issues/{issue_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["message"] == "Issue deleted successfully"

def test_member_can_delete_issue(client):

    register_user(client, "Admin", "admin@company.com", "Admin@123", Role.ADMIN.value)
    register_user(client, "Member", "member@company.com", "Member@123", Role.MEMBER.value)

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

    member_id = get_user_id("member@company.com")

    project_id = create_project(
        client,
        admin_token,
    )

    client.post(
        f"/projects/{project_id}/members",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"user_id": member_id},
    )

    sprint_id = create_sprint(
        client,
        admin_token,
        project_id,
    )

    issue_id = create_issue(
        client,
        admin_token,
        project_id,
        sprint_id,
        member_id,
    )

    response = client.delete(
        f"/issues/{issue_id}",
        headers={"Authorization": f"Bearer {member_token}"},
    )

    assert response.status_code == 200

def test_viewer_cannot_delete_issue(client):

    register_user(client, "Viewer", "viewer@company.com", "Viewer@123", Role.VIEWER.value)

    token = login_user(
        client,
        "viewer@company.com",
        "Viewer@123",
    )

    response = client.delete(
        "/issues/6855dca93a683df1a1111111",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403

def test_member_not_assigned_cannot_delete_issue(client):

    register_user(client, "Admin", "admin@company.com", "Admin@123", Role.ADMIN.value)
    register_user(client, "Member1", "member1@company.com", "Member@123", Role.MEMBER.value)
    register_user(client, "Member2", "member2@company.com", "Member@123", Role.MEMBER.value)

    admin_token = login_user(
        client,
        "admin@company.com",
        "Admin@123",
    )

    member2_token = login_user(
        client,
        "member2@company.com",
        "Member@123",
    )

    member1_id = get_user_id("member1@company.com")

    project_id = create_project(
        client,
        admin_token,
    )

    client.post(
        f"/projects/{project_id}/members",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"user_id": member1_id},
    )

    sprint_id = create_sprint(
        client,
        admin_token,
        project_id,
    )

    issue_id = create_issue(
        client,
        admin_token,
        project_id,
        sprint_id,
        member1_id,
    )

    response = client.delete(
        f"/issues/{issue_id}",
        headers={"Authorization": f"Bearer {member2_token}"},
    )

    assert response.status_code == 403

def test_delete_issue_not_found(client):

    register_user(client, "Admin", "admin@company.com", "Admin@123", Role.ADMIN.value)

    token = login_user(
        client,
        "admin@company.com",
        "Admin@123",
    )

    response = client.delete(
        "/issues/6855dca93a683df1a1111111",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404

def test_delete_issue_without_token(client):

    response = client.delete(
        "/issues/6855dca93a683df1a1111111",
    )

    assert response.status_code == 401
    
def test_delete_issue_invalid_token(client):

    response = client.delete(
        "/issues/6855dca93a683df1a1111111",
        headers={
            "Authorization": "Bearer invalid-token",
        },
    )

    assert response.status_code == 401