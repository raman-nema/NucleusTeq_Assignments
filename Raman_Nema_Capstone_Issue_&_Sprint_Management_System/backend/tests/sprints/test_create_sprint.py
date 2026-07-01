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
            "description": "Issue tracking project.",
        },
    )
    assert response.status_code == 200
    return response.json()["data"]["id"]


# Verify admin can create a sprint.
def test_admin_can_create_sprint(client):
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
    project_id = create_project(
        client,
        token,
    )
    response = client.post(
        f"/projects/{project_id}/sprints",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "name": "Sprint 1",
            "goal": "Complete authentication module.",
            "start_date": "2026-07-01",
            "end_date": "2026-07-14",
        },
    )
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["message"] == "Sprint created successfully"


# Verify assigned member can create a sprint.
def test_assigned_member_can_create_sprint(client):

    register_user(
        client,
        "Admin",
        "admin-member@company.com",
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
        "admin-member@company.com",
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
    response = client.post(
        f"/projects/{project_id}/members",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
        json={
            "user_id": str(member["_id"]),
        },
    )
    assert response.status_code == 200
    response = client.post(
        f"/projects/{project_id}/sprints",
        headers={
            "Authorization": f"Bearer {member_token}",
        },
        json={
            "name": "Sprint 1",
            "goal": "Complete authentication module.",
            "start_date": "2026-07-01",
            "end_date": "2026-07-14",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True


# Verify unassigned member cannot create a sprint.
def test_unassigned_member_cannot_create_sprint(client):
    register_user(
        client,
        "Admin",
        "admin-unassigned@company.com",
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
        "admin-unassigned@company.com",
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

    response = client.post(
        f"/projects/{project_id}/sprints",
        headers={
            "Authorization": f"Bearer {member_token}",
        },
        json={
            "name": "Sprint 1",
            "goal": "Complete authentication module.",
            "start_date": "2026-07-01",
            "end_date": "2026-07-14",
        },
    )

    assert response.status_code == 403


# Verify viewer cannot create a sprint.
def test_viewer_cannot_create_sprint(client):

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
        f"/projects/{ObjectId()}/sprints",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "name": "Sprint 1",
            "goal": "Complete authentication module.",
            "start_date": "2026-07-01",
            "end_date": "2026-07-14",
        },
    )

    assert response.status_code == 403




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

    project_id = create_project(
        client,
        token,
    )

    sprint = {
        "name": "Sprint 1",
        "goal": "Complete authentication module.",
        "start_date": "2026-07-01",
        "end_date": "2026-07-14",
    }

    response = client.post(
        f"/projects/{project_id}/sprints",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=sprint,
    )

    assert response.status_code == 200

    response = client.post(
        f"/projects/{project_id}/sprints",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=sprint,
    )

    assert response.status_code == 409
    assert response.json()["success"] is False
    assert response.json()["message"] == "Sprint already exists"