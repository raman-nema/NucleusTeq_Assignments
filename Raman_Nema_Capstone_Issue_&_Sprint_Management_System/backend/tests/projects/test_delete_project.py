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


# Verify admin can delete a project.
def test_admin_can_delete_project(client):

    register_user(
        client,
        "Admin",
        "admin7@company.com",
        "Admin@123",
        Role.ADMIN.value,
    )

    token = login_user(
        client,
        "admin7@company.com",
        "Admin@123",
    )

    project_id = create_project(client, token)

    response = client.delete(
        f"/projects/{project_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200


# Verify member cannot delete a project.
def test_member_cannot_delete_project(client):

    register_user(
        client,
        "Member",
        "member2@company.com",
        "Admin@123",
        Role.MEMBER.value,
    )

    token = login_user(
        client,
        "member2@company.com",
        "Admin@123",
    )

    response = client.delete(
        "/projects/68614fdcd76d8ab312345678",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403


# Verify viewer cannot delete a project.
def test_viewer_cannot_delete_project(client):

    register_user(
        client,
        "Viewer",
        "viewer2@company.com",
        "Admin@123",
        Role.VIEWER.value,
    )

    token = login_user(
        client,
        "viewer2@company.com",
        "Admin@123",
    )

    response = client.delete(
        "/projects/68614fdcd76d8ab312345678",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403


# Verify deleting a non-existent project returns not found.
def test_delete_project_not_found(client):

    register_user(
        client,
        "Admin",
        "admin8@company.com",
        "Admin@123",
        Role.ADMIN.value,
    )

    token = login_user(
        client,
        "admin8@company.com",
        "Admin@123",
    )

    response = client.delete(
        "/projects/68614fdcd76d8ab312345678",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
