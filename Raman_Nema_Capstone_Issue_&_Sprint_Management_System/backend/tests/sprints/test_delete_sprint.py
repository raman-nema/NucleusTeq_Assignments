import uuid

from app.common.enums import Role


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


# Verify member cannot delete a sprint.
def test_member_cannot_delete_sprint(client):

    register_user(
        client,
        "Member",
        "member@company.com",
        "Admin@123",
        Role.MEMBER.value,
    )

    token = login_user(
        client,
        "member@company.com",
        "Admin@123",
    )

    response = client.delete(
        "/sprints/68614fdcd76d8ab312345678",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403


# Verify viewer cannot delete a sprint.
def test_viewer_cannot_delete_sprint(client):

    register_user(
        client,
        "Viewer",
        "viewer@company.com",
        "Admin@123",
        Role.VIEWER.value,
    )

    token = login_user(
        client,
        "viewer@company.com",
        "Admin@123",
    )

    response = client.delete(
        "/sprints/68614fdcd76d8ab312345678",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403


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
        "/sprints/68614fdcd76d8ab312345678",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
