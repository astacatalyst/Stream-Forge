from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_topology_returns_expected_structure():
    response = client.get("/topology")
    assert response.status_code == 200
    data = response.json()
    assert "kafka" in data
    assert "partitions" in data
    assert "workers" in data
    assert isinstance(data["workers"], list)


def test_nodes_analysis_counts_are_consistent():
    response = client.get("/nodes-analysis")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == data["healthy"] + data["down"]
    assert data["total"] == len(data["workers"])


def test_locations_returns_valid_status_values():
    response = client.get("/locations")
    assert response.status_code == 200
    data = response.json()
    for truck in data:
        assert truck["status"] in ["moving", "idle"]
        assert isinstance(truck["lat"], (int, float))
        assert isinstance(truck["lng"], (int, float))


def test_telemetry_returns_readings_per_truck():
    response = client.get("/telemetry")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for truck in data:
        assert "truck_id" in truck
        assert "readings" in truck


def test_real_telemetry_endpoint_is_reachable():
    response = client.get("/real-telemetry")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_nonexistent_endpoint_returns_404():
    response = client.get("/this-does-not-exist")
    assert response.status_code == 404