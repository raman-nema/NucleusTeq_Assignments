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


def test_admin_can_update_issue(client):

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

    issue_id = create_issue(
        client,
        admin_token,
        project_id,
        sprint_id,
        member_id,
    )

    response = client.put(
        f"/issues/{issue_id}",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
        json={
            "title": "Updated Issue",
            "description": "Updated Description",
            "assignee": member_id,
            "sprint_id": sprint_id,
            "priority": "LOW",
            "status": "IN_PROGRESS",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["title"] == "Updated Issue"
    assert response.json()["data"]["priority"] == "LOW"
    assert response.json()["data"]["status"] == "IN_PROGRESS"

def test_member_can_update_issue(client):

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

    issue_id = create_issue(
        client,
        admin_token,
        project_id,
        sprint_id,
        member_id,
    )

    response = client.put(
        f"/issues/{issue_id}",
        headers={
            "Authorization": f"Bearer {member_token}",
        },
        json={
            "title": "Updated Issue",
            "description": "Updated Description",
            "assignee": member_id,
            "sprint_id": sprint_id,
            "priority": "HIGH",
            "status": "DONE",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True


def test_admin_can_move_done_issue_backward(client):

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

    issue_id = create_issue(
        client,
        admin_token,
        project_id,
        sprint_id,
        member_id,
    )

    client.put(
        f"/issues/{issue_id}",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
        json={
            "title": "Finished Issue",
            "description": "Finished issue description.",
            "assignee": member_id,
            "sprint_id": sprint_id,
            "priority": "HIGH",
            "status": "DONE",
        },
    )

    response = client.put(
        f"/issues/{issue_id}",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
        json={
            "title": "Finished Issue",
            "description": "Finished issue description.",
            "assignee": member_id,
            "sprint_id": sprint_id,
            "priority": "HIGH",
            "status": "IN_PROGRESS",
        },
    )

    assert response.status_code == 200
    assert response.json()["data"]["status"] == "IN_PROGRESS"


def test_member_cannot_move_done_issue_backward(client):

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

    issue_id = create_issue(
        client,
        admin_token,
        project_id,
        sprint_id,
        member_id,
    )

    client.put(
        f"/issues/{issue_id}",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
        json={
            "title": "Finished Issue",
            "description": "Finished issue description.",
            "assignee": member_id,
            "sprint_id": sprint_id,
            "priority": "HIGH",
            "status": "DONE",
        },
    )

    response = client.put(
        f"/issues/{issue_id}",
        headers={
            "Authorization": f"Bearer {member_token}",
        },
        json={
            "title": "Finished Issue",
            "description": "Finished issue description.",
            "assignee": member_id,
            "sprint_id": sprint_id,
            "priority": "HIGH",
            "status": "IN_PROGRESS",
        },
    )

    assert response.status_code == 400
    assert response.json()["message"] == "Issues in DONE state cannot move backward"


def test_viewer_cannot_update_issue(client):

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

    response = client.put(
        "/issues/6855dca93a683df1a1111111",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "Updated Issue",
            "description": "Updated Description",
            "assignee": "6855dca93a683df1a1111112",
            "sprint_id": "6855dca93a683df1a1111113",
            "priority": "HIGH",
            "status": "DONE",
        },
    )

    assert response.status_code == 403

def test_member_not_assigned_cannot_update_issue(client):

    register_user(
        client,
        "Admin",
        "admin@company.com",
        "Admin@123",
        Role.ADMIN.value,
    )

    register_user(
        client,
        "Member1",
        "member1@company.com",
        "Member@123",
        Role.MEMBER.value,
    )

    register_user(
        client,
        "Member2",
        "member2@company.com",
        "Member@123",
        Role.MEMBER.value,
    )

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

    member1_id = get_user_id(
        "member1@company.com",
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
            "user_id": member1_id,
        },
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

    response = client.put(
        f"/issues/{issue_id}",
        headers={
            "Authorization": f"Bearer {member2_token}",
        },
        json={
            "title": "Updated Issue",
            "description": "Updated Description",
            "assignee": member1_id,
            "sprint_id": sprint_id,
            "priority": "HIGH",
            "status": "DONE",
        },
    )

    assert response.status_code == 403


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

    issue_id = create_issue(
        client,
        admin_token,
        project_id,
        sprint_id,
        member_id,
    )

    response = client.put(
        f"/issues/{issue_id}",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
        json={
            "title": "Updated",
            "description": "Updated Description",
            "assignee": member_id,
            "sprint_id": "6855dca93a683df1a1111111",
            "priority": "HIGH",
            "status": "DONE",
        },
    )

    assert response.status_code == 404
