import uuid

from app.common.enums import Role
from app.core.database import database


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


def get_user_id(email):
    user = database.users.find_one({"email": email})
    return str(user["_id"])


def create_project(client, token):
    response = client.post(
        "/projects",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": f"Project-{uuid.uuid4()}",
            "description": "Project Description",
        },
    )
    return response.json()["data"]["id"]


def create_sprint(client, token, project_id):
    response = client.post(
        f"/projects/{project_id}/sprints",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": f"Sprint-{uuid.uuid4()}",
            "goal": "Sprint Goal",
            "start_date": "2026-07-01",
            "end_date": "2026-07-15",
            "status": "PLANNED",
        },
    )
    return response.json()["data"]["id"]


def create_issue(client, token, project_id, sprint_id, assignee_id):
    response = client.post(
        f"/projects/{project_id}/issues",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": f"Issue-{uuid.uuid4()}",
            "description": "Issue Description",
            "assignee": assignee_id,
            "sprint_id": sprint_id,
            "priority": "HIGH",
            "status": "TODO",
        },
    )
    return response.json()["data"]["id"]


def test_member_can_add_comment_to_issue(client):
    register_user(client, "Admin", "admin@company.com", "Admin@123", Role.ADMIN.value)
    register_user(client, "Member", "member@company.com", "Member@123", Role.MEMBER.value)

    admin_token = login_user(client, "admin@company.com", "Admin@123")
    member_token = login_user(client, "member@company.com", "Member@123")
    member_id = get_user_id("member@company.com")

    project_id = create_project(client, admin_token)

    client.post(
        f"/projects/{project_id}/members",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"user_id": member_id},
    )

    sprint_id = create_sprint(client, admin_token, project_id)
    issue_id = create_issue(client, admin_token, project_id, sprint_id, member_id)

    response = client.post(
        f"/issues/{issue_id}/comments",
        headers={"Authorization": f"Bearer {member_token}"},
        json={"text": "This issue needs more context."},
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["comments"][0]["text"] == "This issue needs more context."
    assert response.json()["data"]["comments"][0]["user_name"] == "Member"


def test_member_can_delete_their_comment(client):
    register_user(client, "Admin", "admin@company.com", "Admin@123", Role.ADMIN.value)
    register_user(client, "Member", "member@company.com", "Member@123", Role.MEMBER.value)

    admin_token = login_user(client, "admin@company.com", "Admin@123")
    member_token = login_user(client, "member@company.com", "Member@123")
    member_id = get_user_id("member@company.com")

    project_id = create_project(client, admin_token)

    client.post(
        f"/projects/{project_id}/members",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"user_id": member_id},
    )

    sprint_id = create_sprint(client, admin_token, project_id)
    issue_id = create_issue(client, admin_token, project_id, sprint_id, member_id)

    add_comment_response = client.post(
        f"/issues/{issue_id}/comments",
        headers={"Authorization": f"Bearer {member_token}"},
        json={"text": "Temporary comment."},
    )

    comment_id = add_comment_response.json()["data"]["comments"][0]["id"]

    delete_response = client.delete(
        f"/issues/{issue_id}/comments/{comment_id}",
        headers={"Authorization": f"Bearer {member_token}"},
    )

    assert delete_response.status_code == 200
    assert delete_response.json()["success"] is True
    assert delete_response.json()["data"]["comments"] == []
