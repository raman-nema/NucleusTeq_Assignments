import uuid


# Register a user for login tests.
def register_user(client, email, password):
    client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": email,
            "password": password,
            "role": "MEMBER",
        },
    )


# Verify successful login.
def test_login_success(client):

    # Generate a unique email for each test run.
    email = f"{uuid.uuid4()}@company.com"
    password = "Password@123"

    register_user(client, email, password)

    # Authenticate using the registered credentials.
    response = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["message"] == "Login successful"
    assert "access_token" in response.json()["data"]
    assert response.json()["data"]["role"] == "MEMBER"


# Verify login fails for an invalid email.
def test_login_invalid_email(client):

    response = client.post(
        "/auth/login",
        json={
            "email": "wrong@company.com",
            "password": "Password@123",
        },
    )

    assert response.status_code == 401
    assert response.json()["success"] is False
    assert response.json()["message"] == "Invalid email or password"


# Verify login fails for an invalid password.
def test_login_invalid_password(client):

    # Register the user before testing authentication.
    email = f"{uuid.uuid4()}@company.com"

    register_user(client, email, "Password@123")

    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "WrongPassword",
        },
    )

    assert response.status_code == 401
    assert response.json()["success"] is False
    assert response.json()["message"] == "Invalid email or password"


# Verify login requires an email.
def test_login_missing_email(client):

    response = client.post(
        "/auth/login",
        json={"password": "Password@123"},
    )

    assert response.status_code == 422


# Verify login requires a password.
def test_login_missing_password(client):

    response = client.post(
        "/auth/login",
        json={"email": "test@company.com"},
    )

    assert response.status_code == 422
