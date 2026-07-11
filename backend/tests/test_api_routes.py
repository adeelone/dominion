from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_decree_moderation_blocks_violating_input() -> None:
    response = client.post(
        "/api/worlds/demo/throne/decrees",
        json={"target_id": "p1", "text": "exterminate real group"},
    )
    assert response.status_code == 400


def test_world_export_includes_chronicle_and_projection() -> None:
    response = client.get("/api/worlds/demo/export")
    assert response.status_code == 200
    payload = response.json()
    assert payload["world_id"] == "world-demo"
    assert "settlements" in payload
    assert "chronicle" in payload


def test_report_enters_review_queue() -> None:
    response = client.post("/api/reports", json={"world_id": "world-demo", "reason": "bad listing"})
    assert response.status_code == 200
    assert response.json()["status"] == "queued"
