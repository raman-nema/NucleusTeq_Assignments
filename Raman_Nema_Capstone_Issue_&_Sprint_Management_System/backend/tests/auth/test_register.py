from fastapi.testclient import TestClient
from main import app
client = TestClient(app)

# Verify registration rejects an invalid email.
def test_register_invalid_email():
    response = client.post(
        "/auth/register",
        json={
            "name": "John",
            "email": "invalid-email",
            "password": "Password@123",
            "role": "EMPLOYEE",
        },
    )

    assert response.status_code == 422


# Verify registration requires a name.
def test_register_missing_name():
    response = client.post(
        "/auth/register",
        json={
            "email": "john@company.com",
            "password": "Password@123",
            "role": "EMPLOYEE",
        },
    )

    assert response.status_code == 422


# Verify registration requires a password.
def test_register_missing_password():
    response = client.post(
        "/auth/register",
        json={
            "name": "John",
            "email": "john@company.com",
            "role": "EMPLOYEE",
        },
    )

    assert response.status_code == 422


# Verify registration requires a role.
def test_register_missing_role():
    response = client.post(
        "/auth/register",
        json={
            "name": "John",
            "email": "john@company.com",
            "password": "Password@123",
        },
    )

    assert response.status_code == 422


# Verify registration rejects an invalid role.
def test_register_invalid_role():
    response = client.post(
        "/auth/register",
        json={
            "name": "John",
            "email": "john@company.com",
            "password": "Password@123",
            "role": "ADMINISTRATOR",
        },
    )

    assert response.status_code == 422
