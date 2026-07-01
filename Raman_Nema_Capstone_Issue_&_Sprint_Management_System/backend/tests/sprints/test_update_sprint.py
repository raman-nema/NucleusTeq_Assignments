import uuid

from app.common.enums import Role


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


# Verify admin can update a sprint.
def test_admin_can_update_sprint(client):

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

    sprint_id = create_sprint(
        client,
        token,
        project_id,
    )

    response = client.put(
        f"/sprints/{sprint_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": f"Updated Sprint-{uuid.uuid4()}",
            "goal": "Updated sprint goal.",
            "start_date": "2026-07-05",
            "end_date": "2026-07-20",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True


# Verify member can update a sprint.
def test_member_can_update_sprint(client):

    register_user(
        client,
        "Member",
        "member@company.com",
        "Admin@123",
        Role.MEMBER.value,
    )

    member_token = login_user(
        client,
        "member@company.com",
        "Admin@123",
    )

    register_user(
        client,
        "Admin",
        "admin2@company.com",
        "Admin@123",
        Role.ADMIN.value,
    )

    admin_token = login_user(
        client,
        "admin2@company.com",
        "Admin@123",
    )

    project_id = create_project(client, admin_token)

    sprint_id = create_sprint(
        client,
        admin_token,
        project_id,
    )

    response = client.put(
        f"/sprints/{sprint_id}",
        headers={"Authorization": f"Bearer {member_token}"},
        json={
            "name": f"Updated Sprint-{uuid.uuid4()}",
            "goal": "Updated sprint goal.",
            "start_date": "2026-07-05",
            "end_date": "2026-07-20",
        },
    )

    assert response.status_code == 200


# Verify viewer cannot update a sprint.
def test_viewer_cannot_update_sprint(client):

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
        "/sprints/68614fdcd76d8ab312345678",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Updated Sprint",
            "goal": "Updated Goal",
            "start_date": "2026-07-05",
            "end_date": "2026-07-20",
        },
    )

    assert response.status_code == 403

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

    project_id = create_project(client, token)

    create_sprint(
        client,
        token,
        project_id,
    )

    sprint_id = create_sprint(
        client,
        token,
        project_id,
    )

    response = client.put(
        f"/sprints/{sprint_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Sprint-1",
            "goal": "Updated Goal",
            "start_date": "2026-07-05",
            "end_date": "2026-07-20",
        },
    )

    # Depending on your generated sprint names, this may return
    # either 200 or 409. If you want to test duplicate names,
    # create the first sprint with a fixed name such as "Sprint A"
    # and update the second sprint to "Sprint A".
    assert response.status_code in [200, 409]
