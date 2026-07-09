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

# Create a sprint and return its ID.
def create_sprint(client, token, project_id):
    response = client.post(
        f"/projects/{project_id}/sprints",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": f"Sprint-{uuid.uuid4()}",
            "goal": "Complete authentication module.",
            "start_date": "2026-07-01",
            "end_date": "2026-07-14",
        },
    )
    return response.json()["data"]["id"]


# Verify admin can retrieve all sprints.
def test_admin_can_get_all_sprints(client):
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
    project_id = create_project(client, token)
    create_sprint(
        client,
        token,
        project_id,
    )
    response = client.get(
        f"/projects/{project_id}/sprints",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )
    assert response.status_code == 200
    assert response.json()["success"] is True


# Verify assigned member can retrieve project sprints.
def test_assigned_member_can_get_sprints(client):
    register_user(
        client,
        "Admin",
        "admin2@company.com",
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
        "admin2@company.com",
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
    create_sprint(
        client,
        admin_token,
        project_id,
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
    response = client.get(
        f"/projects/{project_id}/sprints",
        headers={
            "Authorization": f"Bearer {member_token}",
        },
    )
    assert response.status_code == 200
    assert response.json()["success"] is True

# Verify unassigned member cannot retrieve project sprints.
def test_unassigned_member_cannot_get_sprints(client):
    register_user(
        client,
        "Admin",
        "admin3@company.com",
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
        "admin3@company.com",
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
    create_sprint(
        client,
        admin_token,
        project_id,
    )
    response = client.get(
        f"/projects/{project_id}/sprints",
        headers={
            "Authorization": f"Bearer {member_token}",
        },
    )
    assert response.status_code == 403
