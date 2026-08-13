import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app, init_db, DB_PATH  # noqa: E402


@pytest.fixture(autouse=True)
def fresh_db():
    if DB_PATH.exists():
        DB_PATH.unlink()
    init_db()
    yield
    if DB_PATH.exists():
        DB_PATH.unlink()


@pytest.fixture
def client():
    return app.test_client()


def test_create_task(client):
    response = client.post("/api/tasks", json={"title": "Write tests"})
    assert response.status_code == 201
    assert response.get_json()["title"] == "Write tests"


def test_delete_task_actually_persists(client):
    created = client.post("/api/tasks", json={"title": "Temporary task"}).get_json()
    task_id = created["id"]

    client.delete(f"/api/tasks/{task_id}")

    remaining = client.get("/api/tasks").get_json()
    assert all(t["id"] != task_id for t in remaining), "deleted task reappeared -- delete did not persist"


def test_toggle_marks_the_correct_task(client):
    client.post("/api/tasks", json={"title": "First task"})
    second = client.post("/api/tasks", json={"title": "Second task"}).get_json()

    client.patch(f"/api/tasks/{second['id']}/toggle")

    tasks = {t["id"]: t for t in client.get("/api/tasks").get_json()}
    assert tasks[second["id"]]["done"] == 1, "toggling task 2 should mark task 2 done, not task 1"
