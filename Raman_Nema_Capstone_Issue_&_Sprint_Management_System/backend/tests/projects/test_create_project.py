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


# Verify admin can create a project.
def test_admin_can_create_project(client):

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
        "/projects",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Issue Tracker",
            "description": "Issue tracking project.",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["message"] == "Project created successfully"


# Verify member cannot create a project.
def test_member_cannot_create_project(client):

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

    response = client.post(
        "/projects",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Project Alpha",
            "description": "Should fail.",
        },
    )

    assert response.status_code == 403


# Verify viewer cannot create a project.
def test_viewer_cannot_create_project(client):

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

    response = client.post(
        "/projects",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Viewer Project",
            "description": "Should fail.",
        },
    )

    assert response.status_code == 403


# Verify duplicate project names are rejected.
def test_duplicate_project(client):

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

    project = {
        "name": "Duplicate Project",
        "description": "Testing duplicates.",
    }

    client.post(
        "/projects",
        headers={"Authorization": f"Bearer {token}"},
        json=project,
    )

    response = client.post(
        "/projects",
        headers={"Authorization": f"Bearer {token}"},
        json=project,
    )

    assert response.status_code == 409


# Verify authentication is required.
def test_create_project_without_token(client):

    response = client.post(
        "/projects",
        json={
            "name": "Unauthorized Project",
            "description": "Unauthorized request.",
        },
    )

    assert response.status_code == 401
