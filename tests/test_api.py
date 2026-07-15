import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_todos.db")

from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_todo_success(client):
    response = client.post("/api/todos", json={"title": "새 할 일"})
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "새 할 일"
    assert body["completed"] is False
    assert body["id"] is not None


def test_create_todo_empty_fails(client):
    response = client.post("/api/todos", json={"title": "   "})
    assert response.status_code == 422


def test_get_todos_all(client):
    client.post("/api/todos", json={"title": "할 일 1"})
    client.post("/api/todos", json={"title": "할 일 2"})
    response = client.get("/api/todos")
    assert response.status_code == 200
    assert len(response.json()) >= 2


def test_get_todos_active(client):
    client.post("/api/todos", json={"title": "미완료 할 일"})
    response = client.get("/api/todos?status=active")
    assert response.status_code == 200
    assert all(todo["completed"] is False for todo in response.json())


def test_toggle_todo_completion_success(client):
    created = client.post("/api/todos", json={"title": "토글 할 일"}).json()
    response = client.patch(f"/api/todos/{created['id']}", json={"completed": True})
    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_toggle_todo_not_found(client):
    response = client.patch("/api/todos/999999", json={"completed": True})
    assert response.status_code == 404


def test_delete_todo_success(client):
    created = client.post("/api/todos", json={"title": "삭제 할 일"}).json()
    response = client.delete(f"/api/todos/{created['id']}")
    assert response.status_code == 204


def test_delete_todo_not_found(client):
    response = client.delete("/api/todos/999999")
    assert response.status_code == 404


def test_filter_completed_and_remaining_count(client):
    client.post("/api/todos", json={"title": "완료할 일"})
    created = client.post("/api/todos", json={"title": "미완료 할 일"}).json()
    client.patch(f"/api/todos/{created['id']}", json={"completed": True})

    response = client.get("/api/todos?status=completed")
    assert response.status_code == 200
    assert all(todo["completed"] is True for todo in response.json())

    remaining = client.get("/api/todos?status=active")
    assert remaining.status_code == 200
    assert len(remaining.json()) >= 1
