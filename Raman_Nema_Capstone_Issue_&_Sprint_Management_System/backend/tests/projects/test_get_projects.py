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


# Verify all projects can be retrieved.
def test_get_all_projects(client):

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

    create_project(client, token)

    response = client.get(
        "/projects",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["success"] is True


# Verify a project can be retrieved by ID.
def test_get_project_by_id(client):

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

    project_id = create_project(client, token)

    response = client.get(
        f"/projects/{project_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["success"] is True


# Verify a non-existent project returns not found.
def test_project_not_found(client):

    register_user(
        client,
        "Admin",
        "admin3@company.com",
        "Admin@123",
        Role.ADMIN.value,
    )

    token = login_user(
        client,
        "admin3@company.com",
        "Admin@123",
    )

    response = client.get(
        "/projects/68614fdcd76d8ab312345678",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404


# Verify authentication is required.
def test_get_projects_without_token(client):

    response = client.get("/projects")

    assert response.status_code == 401
