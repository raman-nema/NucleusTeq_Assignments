import uuid

from app.common.enums import Role
from app.core.database import database


def register_user(client, name, email, password, role):
    """Register a test user."""

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
    """Login user and return access token."""

    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    return response.json()["data"]["access_token"]


def get_user_id(email):
    """Return user id by email."""

    user = database.users.find_one(
        {
            "email": email,
        }
    )

    return str(user["_id"])


def create_project(client, token):
    """Create a project and return its id."""

    response = client.post(
        "/projects",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "name": f"Project-{uuid.uuid4()}",
            "description": "Project Description",
        },
    )

    return response.json()["data"]["id"]


def assign_member(client, token, project_id, user_id):
    """Assign a member to a project."""

    return client.post(
        f"/projects/{project_id}/members",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "user_id": user_id,
        },
    )


def create_sprint(client, token, project_id):
    """Create a sprint and return its id."""

    response = client.post(
        f"/projects/{project_id}/sprints",
        headers={
            "Authorization": f"Bearer {token}",
        },
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
    """Create an issue and return its id."""

    response = client.post(
        f"/projects/{project_id}/issues",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": f"Issue-{uuid.uuid4()}",
            "description": "Issue Description",
            "assignee": assignee_id,
            "sprint_id": sprint_id,
            "priority": "HIGH",
            "type": "TASK",
            "status": "TODO",
        },
    )

    return response.json()["data"]["id"]


def add_comment(client, token, issue_id, text="Initial comment."):
    """Add a comment and return the response."""

    return client.post(
        f"/issues/{issue_id}/comments",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "text": text,
        },
    )


def setup_comment_issue(client, include_second_member=False):
    """Create admin, member, project, sprint, and issue for comment tests."""

    unique_id = uuid.uuid4().hex
    admin_email = f"admin-{unique_id}@company.com"
    member_email = f"member-{unique_id}@company.com"
    second_member_email = f"member-two-{unique_id}@company.com"
    viewer_email = f"viewer-{unique_id}@company.com"

    register_user(
        client,
        "Admin",
        admin_email,
        "Admin@123",
        Role.ADMIN.value,
    )
    register_user(
        client,
        "Member",
        member_email,
        "Member@123",
        Role.MEMBER.value,
    )
    register_user(
        client,
        "Viewer",
        viewer_email,
        "Viewer@123",
        Role.VIEWER.value,
    )

    admin_token = login_user(client, admin_email, "Admin@123")
    member_token = login_user(client, member_email, "Member@123")
    viewer_token = login_user(client, viewer_email, "Viewer@123")
    member_id = get_user_id(member_email)

    second_member_token = None

    if include_second_member:
        register_user(
            client,
            "Member Two",
            second_member_email,
            "Member@123",
            Role.MEMBER.value,
        )
        second_member_token = login_user(
            client,
            second_member_email,
            "Member@123",
        )
        second_member_id = get_user_id(second_member_email)
    else:
        second_member_id = None

    project_id = create_project(client, admin_token)
    assign_member(client, admin_token, project_id, member_id)

    if second_member_id:
        assign_member(client, admin_token, project_id, second_member_id)

    sprint_id = create_sprint(client, admin_token, project_id)
    issue_id = create_issue(
        client,
        admin_token,
        project_id,
        sprint_id,
        member_id,
    )

    return {
        "admin_token": admin_token,
        "member_token": member_token,
        "second_member_token": second_member_token,
        "viewer_token": viewer_token,
        "issue_id": issue_id,
        "member_id": member_id,
    }


def test_member_can_add_comment_to_issue(client):
    data = setup_comment_issue(client)

    response = add_comment(
        client,
        data["member_token"],
        data["issue_id"],
        "This issue needs more context.",
    )

    comment = response.json()["data"]["comments"][0]

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["message"] == "Comment added successfully"
    assert comment["text"] == "This issue needs more context."
    assert comment["user_name"] == "Member"
    assert comment["user_id"] == data["member_id"]
    assert comment["id"] is not None


def test_admin_can_add_comment_to_issue(client):
    data = setup_comment_issue(client)

    response = add_comment(
        client,
        data["admin_token"],
        data["issue_id"],
        "Admin review comment.",
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["comments"][0]["text"] == "Admin review comment."


def test_viewer_cannot_add_comment_to_issue(client):
    data = setup_comment_issue(client)

    response = add_comment(
        client,
        data["viewer_token"],
        data["issue_id"],
        "Viewer comment.",
    )

    assert response.status_code == 403
    assert response.json()["success"] is False
    assert response.json()["message"] == "Access denied"


def test_unassigned_member_cannot_add_comment_to_issue(client):
    data = setup_comment_issue(client)
    unique_id = uuid.uuid4().hex
    unassigned_email = f"unassigned-{unique_id}@company.com"

    register_user(
        client,
        "Unassigned",
        unassigned_email,
        "Member@123",
        Role.MEMBER.value,
    )
    unassigned_token = login_user(client, unassigned_email, "Member@123")

    response = add_comment(
        client,
        unassigned_token,
        data["issue_id"],
        "Unassigned member comment.",
    )

    assert response.status_code == 403
    assert response.json()["success"] is False
    assert response.json()["message"] == "Access denied"


def test_add_comment_returns_not_found_for_missing_issue(client):
    data = setup_comment_issue(client)

    response = add_comment(
        client,
        data["member_token"],
        "6855dca93a683df1a1111111",
        "Missing issue comment.",
    )

    assert response.status_code == 404
    assert response.json()["success"] is False
    assert response.json()["message"] == "Issue not found"


def test_member_can_update_their_comment(client):
    data = setup_comment_issue(client)
    add_response = add_comment(
        client,
        data["member_token"],
        data["issue_id"],
        "Original comment.",
    )
    comment_id = add_response.json()["data"]["comments"][0]["id"]

    response = client.put(
        f"/issues/{data['issue_id']}/comments/{comment_id}",
        headers={
            "Authorization": f"Bearer {data['member_token']}",
        },
        json={
            "text": "Updated comment.",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["message"] == "Comment updated successfully"
    assert response.json()["data"]["comments"][0]["text"] == "Updated comment."


def test_admin_can_update_member_comment(client):
    data = setup_comment_issue(client)
    add_response = add_comment(
        client,
        data["member_token"],
        data["issue_id"],
        "Member comment.",
    )
    comment_id = add_response.json()["data"]["comments"][0]["id"]

    response = client.put(
        f"/issues/{data['issue_id']}/comments/{comment_id}",
        headers={
            "Authorization": f"Bearer {data['admin_token']}",
        },
        json={
            "text": "Admin updated comment.",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["comments"][0]["text"] == "Admin updated comment."


def test_member_cannot_update_another_member_comment(client):
    data = setup_comment_issue(client, include_second_member=True)
    add_response = add_comment(
        client,
        data["member_token"],
        data["issue_id"],
        "Member comment.",
    )
    comment_id = add_response.json()["data"]["comments"][0]["id"]

    response = client.put(
        f"/issues/{data['issue_id']}/comments/{comment_id}",
        headers={
            "Authorization": f"Bearer {data['second_member_token']}",
        },
        json={
            "text": "Second member update.",
        },
    )

    assert response.status_code == 403
    assert response.json()["success"] is False
    assert response.json()["message"] == "Access denied"


def test_viewer_cannot_update_comment(client):
    data = setup_comment_issue(client)
    add_response = add_comment(
        client,
        data["member_token"],
        data["issue_id"],
        "Member comment.",
    )
    comment_id = add_response.json()["data"]["comments"][0]["id"]

    response = client.put(
        f"/issues/{data['issue_id']}/comments/{comment_id}",
        headers={
            "Authorization": f"Bearer {data['viewer_token']}",
        },
        json={
            "text": "Viewer update.",
        },
    )

    assert response.status_code == 403
    assert response.json()["success"] is False
    assert response.json()["message"] == "Access denied"


def test_update_comment_returns_not_found_for_missing_issue(client):
    data = setup_comment_issue(client)

    response = client.put(
        "/issues/6855dca93a683df1a1111111/comments/6855dca93a683df1a2222222",
        headers={
            "Authorization": f"Bearer {data['member_token']}",
        },
        json={
            "text": "Updated comment.",
        },
    )

    assert response.status_code == 404
    assert response.json()["success"] is False
    assert response.json()["message"] == "Issue not found"


def test_update_comment_returns_not_found_for_missing_comment(client):
    data = setup_comment_issue(client)

    response = client.put(
        f"/issues/{data['issue_id']}/comments/6855dca93a683df1a1111111",
        headers={
            "Authorization": f"Bearer {data['member_token']}",
        },
        json={
            "text": "Updated comment.",
        },
    )

    assert response.status_code == 404
    assert response.json()["success"] is False
    assert response.json()["message"] == "Comment not found"


def test_member_can_delete_their_comment(client):
    data = setup_comment_issue(client)
    add_response = add_comment(
        client,
        data["member_token"],
        data["issue_id"],
        "Temporary comment.",
    )
    comment_id = add_response.json()["data"]["comments"][0]["id"]

    response = client.delete(
        f"/issues/{data['issue_id']}/comments/{comment_id}",
        headers={
            "Authorization": f"Bearer {data['member_token']}",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["message"] == "Comment deleted successfully"
    assert response.json()["data"]["comments"] == []


def test_admin_can_delete_member_comment(client):
    data = setup_comment_issue(client)
    add_response = add_comment(
        client,
        data["member_token"],
        data["issue_id"],
        "Comment to delete.",
    )
    comment_id = add_response.json()["data"]["comments"][0]["id"]

    response = client.delete(
        f"/issues/{data['issue_id']}/comments/{comment_id}",
        headers={
            "Authorization": f"Bearer {data['admin_token']}",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["comments"] == []


def test_member_cannot_delete_another_member_comment(client):
    data = setup_comment_issue(client, include_second_member=True)
    add_response = add_comment(
        client,
        data["member_token"],
        data["issue_id"],
        "Member comment.",
    )
    comment_id = add_response.json()["data"]["comments"][0]["id"]

    response = client.delete(
        f"/issues/{data['issue_id']}/comments/{comment_id}",
        headers={
            "Authorization": f"Bearer {data['second_member_token']}",
        },
    )

    assert response.status_code == 403
    assert response.json()["success"] is False
    assert response.json()["message"] == "Access denied"


def test_unassigned_member_cannot_delete_comment(client):
    data = setup_comment_issue(client)
    unique_id = uuid.uuid4().hex
    unassigned_email = f"unassigned-delete-{unique_id}@company.com"
    add_response = add_comment(
        client,
        data["member_token"],
        data["issue_id"],
        "Member comment.",
    )
    comment_id = add_response.json()["data"]["comments"][0]["id"]

    register_user(
        client,
        "Unassigned",
        unassigned_email,
        "Member@123",
        Role.MEMBER.value,
    )
    unassigned_token = login_user(client, unassigned_email, "Member@123")

    response = client.delete(
        f"/issues/{data['issue_id']}/comments/{comment_id}",
        headers={
            "Authorization": f"Bearer {unassigned_token}",
        },
    )

    assert response.status_code == 403
    assert response.json()["success"] is False
    assert response.json()["message"] == "Access denied"


def test_viewer_cannot_delete_comment(client):
    data = setup_comment_issue(client)
    add_response = add_comment(
        client,
        data["member_token"],
        data["issue_id"],
        "Member comment.",
    )
    comment_id = add_response.json()["data"]["comments"][0]["id"]

    response = client.delete(
        f"/issues/{data['issue_id']}/comments/{comment_id}",
        headers={
            "Authorization": f"Bearer {data['viewer_token']}",
        },
    )

    assert response.status_code == 403
    assert response.json()["success"] is False
    assert response.json()["message"] == "Access denied"


def test_unauthenticated_user_cannot_delete_comment(client):
    data = setup_comment_issue(client)
    add_response = add_comment(
        client,
        data["member_token"],
        data["issue_id"],
        "Member comment.",
    )
    comment_id = add_response.json()["data"]["comments"][0]["id"]

    response = client.delete(
        f"/issues/{data['issue_id']}/comments/{comment_id}",
    )

    assert response.status_code == 401
    assert response.json()["success"] is False
    assert response.json()["message"] == "Authentication required"


def test_delete_comment_returns_not_found_for_missing_issue(client):
    data = setup_comment_issue(client)

    response = client.delete(
        "/issues/6855dca93a683df1a1111111/comments/6855dca93a683df1a2222222",
        headers={
            "Authorization": f"Bearer {data['member_token']}",
        },
    )

    assert response.status_code == 404
    assert response.json()["success"] is False
    assert response.json()["message"] == "Issue not found"

