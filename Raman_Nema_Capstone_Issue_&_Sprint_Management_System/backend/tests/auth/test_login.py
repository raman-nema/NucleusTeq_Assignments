import uuid


def register_user(client, email, password):
    """Registers a user for login testing."""

    client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": email,
            "password": password,
            "role": "MEMBER",
        },
    )


def test_login_success(client):
    """Test successful login."""

    # Use a unique email so this test does not conflict with other test runs.
    email = f"{uuid.uuid4()}@test.com"
    password = "Password@123"

    register_user(client, email, password)

    # Log in with the same credentials used during registration.
    response = client.post("/auth/login", json={"email": email, "password": password})

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["message"] == "Login successful"
    assert "access_token" in response.json()["data"]
    assert response.json()["data"]["role"] == "MEMBER"


def test_login_invalid_email(client):
    """Test login with invalid email."""

    response = client.post(
        "/auth/login", json={"email": "wrong@test.com", "password": "Password@123"}
    )

    assert response.status_code == 401
    assert response.json()["success"] is False
    assert response.json()["message"] == "Invalid email or password"


def test_login_invalid_password(client):
    """Test login with invalid password."""

    # Register the user first so only the password validation fails.
    email = f"{uuid.uuid4()}@test.com"

    register_user(client, email, "Password@123")

    response = client.post(
        "/auth/login", json={"email": email, "password": "WrongPassword"}
    )

    assert response.status_code == 401
    assert response.json()["success"] is False
    assert response.json()["message"] == "Invalid email or password"


def test_login_missing_email(client):
    """Test login with missing email."""

    # FastAPI should reject requests that do not include all required fields.
    response = client.post("/auth/login", json={"password": "Password@123"})

    assert response.status_code == 422


def test_login_missing_password(client):
    """Test login with missing password."""

    response = client.post("/auth/login", json={"email": "test@test.com"})

    assert response.status_code == 422
