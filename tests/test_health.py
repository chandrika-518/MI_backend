from uuid import uuid4

from fastapi.testclient import TestClient
from jose import jwt

from app.core.settings import settings
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_login_endpoint():
    response = client.post(
        "/api/auth/login",
        json={"email": "user@example.com", "password": "Password123!"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["token_type"] == "Bearer"
    assert payload["user"]["email"] == "user@example.com"

    decoded = jwt.decode(
        payload["access_token"],
        settings.secrets.get_jwt_secret(),
        algorithms=[settings.jwt_algorithm],
    )
    assert decoded["sub"] == "user@example.com"


def test_login_with_long_password_is_supported():
    long_password = "a" * 80
    unique_email = f"longpassword-{uuid4().hex[:8]}@example.com"
    register_response = client.post(
        "/api/auth/register",
        json={"email": unique_email, "password": long_password},
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/api/auth/login",
        json={"email": unique_email, "password": long_password},
    )
    assert login_response.status_code == 200


def test_invalid_login_returns_unauthorized():
    response = client.post(
        "/api/auth/login",
        json={"email": "user@example.com", "password": "wrong-password"},
    )
    assert response.status_code == 401


def test_registration_creates_new_user():
    unique_email = f"newuser-{uuid4().hex[:8]}@example.com"
    response = client.post(
        "/api/auth/register",
        json={"email": unique_email, "password": "NewPassword123!"},
    )
    assert response.status_code == 201
    payload = response.json()
    assert payload["user"]["email"] == unique_email


def test_research_endpoint_requires_auth_token():
    response = client.post(
        "/api/research",
        json={
            "competitors": ["OpenAI"],
            "topics": ["AI"],
            "urls": ["https://example.com"],
            "context": "test context",
        },
    )
    assert response.status_code == 401


def test_research_endpoint_with_valid_token():
    login_response = client.post(
        "/api/auth/login",
        json={"email": "user@example.com", "password": "Password123!"},
    )
    token = login_response.json()["access_token"]

    response = client.post(
        "/api/research",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "competitors": ["OpenAI"],
            "topics": ["AI"],
            "urls": ["https://example.com"],
            "context": "test context",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["hallucinationCheck"]["status"] == "Supported"
    assert payload["themes"][0]["title"] == "Enterprise AI"


def test_history_endpoint_requires_auth_token():
    response = client.get("/api/history")
    assert response.status_code == 401


def test_history_endpoint_with_valid_token():
    login_response = client.post(
        "/api/auth/login",
        json={"email": "user@example.com", "password": "Password123!"},
    )
    token = login_response.json()["access_token"]

    response = client.get("/api/history", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    payload = response.json()
    assert payload[0]["title"] == "Enterprise AI Research"
