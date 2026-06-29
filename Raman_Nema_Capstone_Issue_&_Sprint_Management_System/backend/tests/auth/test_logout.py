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


def test_logout_success(client):

    register_user(
        client,
        "Logout User",
        "logout@test.com",
        "Admin@123",
        Role.ADMIN.value,
    )

    token = login_user(
        client,
        "logout@test.com",
        "Admin@123",
    )

    response = client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Logout successful"


def test_logout_without_token(client):

    response = client.post("/auth/logout")

    assert response.status_code == 401


def test_logout_invalid_token(client):

    response = client.post(
        "/auth/logout",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401


def test_logged_out_token_cannot_access_dashboard(client):

    register_user(
        client,
        "Protected User",
        "protected@test.com",
        "Admin@123",
        Role.ADMIN.value,
    )

    token = login_user(
        client,
        "protected@test.com",
        "Admin@123",
    )

    client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
    )

    response = client.get(
        "/admin/dashboard",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
