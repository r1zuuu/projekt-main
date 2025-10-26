"""Integration tests for the task endpoints."""

from __future__ import annotations


def _create_and_login_user(client):
    response = client.post(
        "/users/register",
        json={"username": "tasker", "password": "strongpw"},
    )
    user_id = response.get_json()["id"]
    login = client.post(
        "/users/login",
        json={"username": "tasker", "password": "strongpw"},
    )
    assert login.status_code == 200
    return user_id


def test_task_crud_flow(client):
    user_id = _create_and_login_user(client)

    create_resp = client.post(
        "/tasks/",
        json={
            "task_name": "Write docs",
            "user_id": user_id,
            "status": "pending",
            "priority": "high",
        },
    )
    assert create_resp.status_code == 201
    task_payload = create_resp.get_json()
    task_id = task_payload["task_id"]
    assert task_payload["priority"] == "high"

    list_resp = client.get("/tasks/")
    assert list_resp.status_code == 200
    tasks = list_resp.get_json()
    assert any(item["task_id"] == task_id for item in tasks)

    update_resp = client.put(
        f"/tasks/{task_id}",
        json={"status": "completed", "priority": "medium"},
    )
    assert update_resp.status_code == 200
    updated = update_resp.get_json()
    assert updated["status"] == "completed"
    assert updated["priority"] == "medium"

    delete_resp = client.delete(f"/tasks/{task_id}")
    assert delete_resp.status_code == 200
    assert delete_resp.get_json()["message"] == "Task deleted successfully."

    not_found = client.get(f"/tasks/{task_id}")
    assert not_found.status_code == 404


def test_validation_errors(client):
    user_id = _create_and_login_user(client)

    missing_name = client.post("/tasks/", json={"user_id": user_id})
    assert missing_name.status_code == 400

    invalid_status = client.post(
        "/tasks/",
        json={
            "task_name": "Test invalid",
            "user_id": user_id,
            "status": "unknown",
        },
    )
    assert invalid_status.status_code == 400

    invalid_user = client.post(
        "/tasks/",
        json={"task_name": "Missing user", "user_id": 9999},
    )
    assert invalid_user.status_code == 404
