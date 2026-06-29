from app.common.enums import Role


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


def login_user(client, email, password):
    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    return response.json()["data"]["access_token"]


def test_admin_can_access_dashboard(client):

    register_user(
        client,
        "Admin User",
        "admin1@test.com",
        "Admin@123",
        Role.ADMIN.value,
    )

    token = login_user(
        client,
        "admin1@test.com",
        "Admin@123",
    )

    response = client.get(
        "/admin/dashboard",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200


def test_manager_cannot_access_dashboard(client):

    register_user(
        client,
        "Manager",
        "manager@test.com",
        "Admin@123",
        Role.MEMBER.value,
    )

    token = login_user(
        client,
        "manager@test.com",
        "Admin@123",
    )

    response = client.get(
        "/admin/dashboard",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403


def test_viewer_cannot_access_dashboard(client):

    register_user(
        client,
        "Viewer",
        "viewer@test.com",
        "Admin@123",
        Role.VIEWER.value,
    )

    token = login_user(
        client,
        "viewer@test.com",
        "Admin@123",
    )

    response = client.get(
        "/admin/dashboard",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403


def test_dashboard_without_token(client):

    response = client.get("/admin/dashboard")

    assert response.status_code == 401


def test_dashboard_invalid_token(client):

    response = client.get(
        "/admin/dashboard",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401
