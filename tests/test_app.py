from app import app


def test_home_page_returns_200():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"OpsPulse" in response.data


def test_health_returns_healthy():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json == {"status": "healthy"}


def test_ready_returns_ready():
    client = app.test_client()

    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json == {"status": "ready"}


def test_api_status_returns_version():
    client = app.test_client()

    response = client.get("/api/status")

    assert response.status_code == 200
    assert response.json == {"status": "ok", "version": "0.1.0"}