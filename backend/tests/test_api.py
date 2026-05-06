from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health() -> None:
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_draft_endpoint_returns_permutation() -> None:
    teams = ["North", "South", "East", "West"]
    r = client.post("/api/draft", json={"teams": teams})
    assert r.status_code == 200
    data = r.json()
    assert data["odds"] == [37, 28, 20, 15]
    assert set(data["draftOrder"]) == set(teams)
    assert len(data["draftOrder"]) == 4


def test_draft_endpoint_rejects_invalid_input() -> None:
    r = client.post("/api/draft", json={"teams": ["A", "B", "C"]})
    assert r.status_code == 422

    r2 = client.post("/api/draft", json={"teams": ["A", "A", "B", "C"]})
    assert r2.status_code == 400
