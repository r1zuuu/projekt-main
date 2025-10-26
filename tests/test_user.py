"""Integration tests covering the user endpoints."""

from __future__ import annotations


def test_register_and_login_flow(client):
    response = client.post(
        "/users/register",
        json={"username": "alice", "password": "secret1"},
    )
    assert response.status_code == 201
    payload = response.get_json()
    assert payload["username"] == "alice"

    login_response = client.post(
        "/users/login",
        json={"username": "alice", "password": "secret1"},
    )
    assert login_response.status_code == 200
    logged_in = login_response.get_json()
    assert logged_in["username"] == "alice"

    with client.session_transaction() as session:
        assert session.get("user_id") == payload["id"]


def test_profile_requires_authentication(client):
    response = client.get("/users/profile")
    assert response.status_code == 401
    assert response.get_json()["error"] == "Authentication required."


def test_duplicate_registration_returns_error(client):
    data = {"username": "bob", "password": "secret1"}
    assert client.post("/users/register", json=data).status_code == 201

    duplicate = client.post("/users/register", json=data)
    assert duplicate.status_code == 400
    body = duplicate.get_json()
    assert "already" in body["error"].lower()
