from app.common.enums import Role


# Register a user for logout tests.
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


# Verify successful logout.
def test_logout_success(client):

    register_user(
        client,
        "Logout User",
        "logout@company.com",
        "Admin@123",
        Role.ADMIN.value,
    )

    token = login_user(
        client,
        "logout@company.com",
        "Admin@123",
    )

    response = client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Logout successful"


# Verify logout requires authentication.
def test_logout_without_token(client):

    response = client.post("/auth/logout")

    assert response.status_code == 401


# Verify invalid tokens are rejected.
def test_logout_invalid_token(client):

    response = client.post(
        "/auth/logout",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401


# Verify logged-out tokens cannot access protected endpoints.
def test_logged_out_token_cannot_access_dashboard(client):

    register_user(
        client,
        "Protected User",
        "protected@company.com",
        "Admin@123",
        Role.ADMIN.value,
    )

    token = login_user(
        client,
        "protected@company.com",
        "Admin@123",
    )

    # Invalidate the access token.
    client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
    )

    response = client.get(
        "/admin/dashboard",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
