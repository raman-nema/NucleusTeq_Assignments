from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


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


def test_register_missing_name():
    response = client.post(
        "/auth/register",
        json={
            "email": "john@example.com",
            "password": "Password@123",
            "role": "EMPLOYEE",
        },
    )

    assert response.status_code == 422


def test_register_missing_password():
    response = client.post(
        "/auth/register",
        json={"name": "John", "email": "john@example.com", "role": "EMPLOYEE"},
    )

    assert response.status_code == 422


def test_register_missing_role():
    response = client.post(
        "/auth/register",
        json={"name": "John", "email": "john@example.com", "password": "Password@123"},
    )

    assert response.status_code == 422


def test_register_invalid_role():
    response = client.post(
        "/auth/register",
        json={
            "name": "John",
            "email": "john@example.com",
            "password": "Password@123",
            "role": "ADMINISTRATOR",
        },
    )

    assert response.status_code == 422
