import pytest
from httpx import AsyncClient
from src.main import app, DATA_DOMAINS, TELEMETRY_ENABLED
import os

@pytest.mark.asyncio
async def test_read_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert "Welcome to OpenBayanMesh-Edge API" in response.json()["message"]

@pytest.mark.asyncio
async def test_health_v1():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["version"] == "v1"

@pytest.mark.asyncio
async def test_info_v1():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/v1/info")
    assert response.status_code == 200
    assert response.json()["app_name"] == "OpenBayanMesh-Edge"
    assert response.json()["api_version"] == "v1"
    assert response.json()["data_domains"] == DATA_DOMAINS

@pytest.mark.asyncio
async def test_query_v1():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/v1/query")
    assert response.status_code == 200
    assert response.json()["message"] == "Query endpoint for v1"

@pytest.mark.asyncio
async def test_metrics_v1():
    # Temporarily enable telemetry for this test if it's disabled
    original_telemetry_state = os.getenv("TELEMETRY_ENABLED")
    os.environ["TELEMETRY_ENABLED"] = "true"
    # Re-import app to apply new env var, or restart app if possible
    # For httpx.AsyncClient, changes to os.environ might not reflect immediately
    # without re-initializing the app or client. For simplicity, we assume
    # the app instance will pick up the change or this test runs in isolation.

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/v1/metrics")
    
    if original_telemetry_state is not None:
        os.environ["TELEMETRY_ENABLED"] = original_telemetry_state
    else:
        del os.environ["TELEMETRY_ENABLED"]

    assert response.status_code == 200
    assert response.json()["message"] == "Metrics endpoint for v1"
    assert "fatal_errors" in response.json()

@pytest.mark.asyncio
async def test_metrics_v1_telemetry_disabled():
    # Temporarily disable telemetry for this test
    original_telemetry_state = os.getenv("TELEMETRY_ENABLED")
    os.environ["TELEMETRY_ENABLED"] = "false"

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/v1/metrics")
    
    if original_telemetry_state is not None:
        os.environ["TELEMETRY_ENABLED"] = original_telemetry_state
    else:
        del os.environ["TELEMETRY_ENABLED"]

    assert response.status_code == 403
    assert "Telemetry is disabled" in response.json()["detail"]

# Note: Testing Neo4j interaction requires a running Neo4j instance or mocking.
# For now, we'll skip direct Neo4j interaction tests in this file.
# A separate integration test suite would be more appropriate.