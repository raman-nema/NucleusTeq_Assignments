import uuid

from bson import ObjectId

from app.common.enums import Role
from app.repositories.user_repository import UserRepository


# Register a user for testing.
def register_user(client, name, email, password, role):
    client.post(
        "/auth/register",
        json={
            "name": name,
            "email": email,
            "password": password,
            "role": role,
        },
    )


# Authenticate a user and return the access token.
def login_user(client, email, password):
    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    return response.json()["data"]["access_token"]


# Create a project and return its ID.
def create_project(client, token):

    project_name = f"Project-{uuid.uuid4()}"

    response = client.post(
        "/projects",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": project_name,
            "description": "Project Description",
        },
    )

    return response.json()["data"]["id"]


# Create a sprint and return its ID.
def create_sprint(client, token, project_id):

    response = client.post(
        f"/projects/{project_id}/sprints",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": f"Sprint-{uuid.uuid4()}",
            "goal": "Complete authentication module.",
            "start_date": "2026-07-01",
            "end_date": "2026-07-14",
        },
    )

    return response.json()["data"]["id"]


def create_issue(client, token, project_id, sprint_id, assignee_id):
    response = client.post(
        f"/projects/{project_id}/issues",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": f"Issue-{uuid.uuid4()}",
            "description": "Issue description for sprint deletion check.",
            "assignee": assignee_id,
            "sprint_id": sprint_id,
            "priority": "MEDIUM",
            "type": "TASK",
            "status": "TODO",
        },
    )

    return response.json()["data"]["id"]


# Verify admin can delete a sprint.
def test_admin_can_delete_sprint(client):

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

    project_id = create_project(client, token)

    sprint_id = create_sprint(
        client,
        token,
        project_id,
    )

    response = client.delete(
        f"/sprints/{sprint_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["message"] == "Sprint deleted successfully"


# Verify assigned member can delete a sprint.
def test_assigned_member_can_delete_sprint(client):

    register_user(
        client,
        "Admin",
        "admin-member@company.com",
        "Admin@123",
        Role.ADMIN.value,
    )

    register_user(
        client,
        "Member",
        "member@company.com",
        "Admin@123",
        Role.MEMBER.value,
    )

    admin_token = login_user(
        client,
        "admin-member@company.com",
        "Admin@123",
    )

    member_token = login_user(
        client,
        "member@company.com",
        "Admin@123",
    )

    project_id = create_project(
        client,
        admin_token,
    )

    sprint_id = create_sprint(
        client,
        admin_token,
        project_id,
    )

    member = UserRepository.find_by_email(
        "member@company.com",
    )

    response = client.post(
        f"/projects/{project_id}/members",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
        json={
            "user_id": str(member["_id"]),
        },
    )

    assert response.status_code == 200

    response = client.delete(
        f"/sprints/{sprint_id}",
        headers={
            "Authorization": f"Bearer {member_token}",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True


def test_sprint_with_issue_cannot_be_deleted(client):
    admin_email = f"admin-sprint-issue-{uuid.uuid4()}@company.com"
    member_email = f"member-sprint-issue-{uuid.uuid4()}@company.com"

    register_user(
        client,
        "Admin",
        admin_email,
        "Admin@123",
        Role.ADMIN.value,
    )

    register_user(
        client,
        "Member",
        member_email,
        "Admin@123",
        Role.MEMBER.value,
    )

    admin_token = login_user(
        client,
        admin_email,
        "Admin@123",
    )

    project_id = create_project(
        client,
        admin_token,
    )

    sprint_id = create_sprint(
        client,
        admin_token,
        project_id,
    )

    member = UserRepository.find_by_email(member_email)

    response = client.post(
        f"/projects/{project_id}/members",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
        json={
            "user_id": str(member["_id"]),
        },
    )

    assert response.status_code == 200

    create_issue(
        client,
        admin_token,
        project_id,
        sprint_id,
        str(member["_id"]),
    )

    response = client.delete(
        f"/sprints/{sprint_id}",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
    )

    assert response.status_code == 409
    assert response.json()["success"] is False
    assert response.json()["message"] == (
        "Sprint cannot be deleted because an issue is present"
    )

# Verify deleting a non-existent sprint returns not found.
def test_delete_sprint_not_found(client):

    register_user(
        client,
        "Admin",
        "admin2@company.com",
        "Admin@123",
        Role.ADMIN.value,
    )

    token = login_user(
        client,
        "admin2@company.com",
        "Admin@123",
    )

    response = client.delete(
        f"/sprints/{ObjectId()}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 404
