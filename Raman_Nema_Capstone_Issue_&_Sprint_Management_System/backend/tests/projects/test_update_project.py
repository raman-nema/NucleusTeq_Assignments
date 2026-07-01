import uuid

from bson import ObjectId

from app.common.enums import Role
from app.repositories.user_repository import UserRepository


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


# Verify admin can update a project.
def test_admin_can_update_project(client):

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

    project_id = create_project(
        client,
        token,
    )

    response = client.put(
        f"/projects/{project_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "name": f"Updated-{uuid.uuid4()}",
            "description": "Updated Description",
        },
    )

    assert response.status_code == 200


# Verify assigned member can update a project.
def test_assigned_member_can_update_project(client):

    register_user(
        client,
        "Admin",
        "admin5@company.com",
        "Admin@123",
        Role.ADMIN.value,
    )

    register_user(
        client,
        "Member",
        "member@company.com",
        "Admin@123",
        Role.MEMBER.value,
    )

    admin_token = login_user(
        client,
        "admin5@company.com",
        "Admin@123",
    )

    member_token = login_user(
        client,
        "member@company.com",
        "Admin@123",
    )

    project_id = create_project(
        client,
        admin_token,
    )

    member = UserRepository.find_by_email(
        "member@company.com",
    )

    client.post(
        f"/projects/{project_id}/members",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
        json={
            "user_id": str(member["_id"]),
        },
    )

    response = client.put(
        f"/projects/{project_id}",
        headers={
            "Authorization": f"Bearer {member_token}",
        },
        json={
            "name": f"Updated-{uuid.uuid4()}",
            "description": "Updated Description",
        },
    )

    assert response.status_code == 200


# Verify unassigned member cannot update a project.
def test_unassigned_member_cannot_update_project(client):

    register_user(
        client,
        "Admin",
        "admin6@company.com",
        "Admin@123",
        Role.ADMIN.value,
    )

    register_user(
        client,
        "Member",
        "member2@company.com",
        "Admin@123",
        Role.MEMBER.value,
    )

    admin_token = login_user(
        client,
        "admin6@company.com",
        "Admin@123",
    )

    member_token = login_user(
        client,
        "member2@company.com",
        "Admin@123",
    )

    project_id = create_project(
        client,
        admin_token,
    )

    response = client.put(
        f"/projects/{project_id}",
        headers={
            "Authorization": f"Bearer {member_token}",
        },
        json={
            "name": f"Updated-{uuid.uuid4()}",
            "description": "Updated Description",
        },
    )

    assert response.status_code == 403


# Verify viewer cannot update a project.
def test_viewer_cannot_update_project(client):

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

    response = client.put(
        f"/projects/{ObjectId()}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "name": "Updated",
            "description": "Updated",
        },
    )

    assert response.status_code == 403