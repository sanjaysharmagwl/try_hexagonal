import uuid

import pytest
from api.deps import get_idea_repository
from api.main import app
from core.ideas.repository import InMemoryIdeaRepository
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    repo = InMemoryIdeaRepository()
    app.dependency_overrides[get_idea_repository] = lambda: repo
    yield TestClient(app), repo
    app.dependency_overrides.clear()


def test_successful_submission(client):
    """Requirement: Idea Submission — successful submission scenario."""
    test_client, repo = client
    response = test_client.post(
        "/ideas",
        json={"title": "New idea", "description": "Details", "author_id": "u1"},
    )
    assert response.status_code == 201
    body = response.json()
    assert uuid.UUID(body["id"])
    assert body["status"] == "submitted"
    assert body["title"] == "New idea"
    assert body["description"] == "Details"
    assert repo.get(uuid.UUID(body["id"])) is not None


def test_description_omitted_defaults_to_empty(client):
    """Requirement: Idea Submission — description omitted scenario."""
    test_client, _ = client
    response = test_client.post("/ideas", json={"title": "New idea", "author_id": "u1"})
    assert response.status_code == 201
    assert response.json()["description"] == ""


def test_empty_title_rejected(client):
    """Requirement: Idea Submission — title violates request schema scenario."""
    test_client, _ = client
    response = test_client.post("/ideas", json={"title": "", "description": "", "author_id": "u1"})
    assert response.status_code == 422


def test_whitespace_title_rejected_by_domain(client):
    """Requirement: Idea Submission — blank title rejected by domain scenario."""
    test_client, _ = client
    response = test_client.post(
        "/ideas", json={"title": "   ", "description": "", "author_id": "u1"}
    )
    assert response.status_code == 422
    assert "cannot be empty" in response.json()["detail"]


def test_title_is_stripped(client):
    """Requirement: Idea Submission — title normalized scenario."""
    test_client, _ = client
    response = test_client.post(
        "/ideas", json={"title": "  Padded  ", "description": "", "author_id": "u1"}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Padded"
