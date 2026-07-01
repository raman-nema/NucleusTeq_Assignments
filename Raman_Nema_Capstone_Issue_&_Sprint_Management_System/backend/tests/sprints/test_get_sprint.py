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


# Verify all sprints of a project can be retrieved.
def test_get_all_sprints(client):

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

    create_sprint(
        client,
        token,
        project_id,
    )

    response = client.get(
        f"/projects/{project_id}/sprints",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["success"] is True


# Verify a sprint can be retrieved by ID.
def test_get_sprint_by_id(client):

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

    sprint_id = create_sprint(
        client,
        token,
        project_id,
    )

    response = client.get(
        f"/sprints/{sprint_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["success"] is True


# Verify a non-existent sprint returns not found.
def test_sprint_not_found(client):

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
        "/sprints/68614fdcd76d8ab312345678",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404


# Verify a non-existent project returns not found.
def test_project_not_found_for_sprints(client):

    register_user(
        client,
        "Admin",
        "admin4@company.com",
        "Admin@123",
        Role.ADMIN.value,
    )

    token = login_user(
        client,
        "admin4@company.com",
        "Admin@123",
    )

    response = client.get(
        "/projects/68614fdcd76d8ab312345678/sprints",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404


# Verify authentication is required.
def test_get_sprints_without_token(client):

    response = client.get("/projects/68614fdcd76d8ab312345678/sprints")

    assert response.status_code == 401
