import pytest
from httpx import AsyncClient
from src.main import app

@pytest.mark.asyncio
async def test_get_versions():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/versions")
    assert response.status_code == 200
    versions = response.json()["versions"]
    assert any(v["version"] == "v1" and v["status"] == "active" for v in versions)
    assert any(v["version"] == "v2" and v["status"] == "deprecated" for v in versions)

@pytest.mark.asyncio
async def test_deprecated_v2_health_returns_410():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/v2/health")
    assert response.status_code == 410
    assert "API Version v2 is deprecated" in response.json()["detail"]

@pytest.mark.asyncio
async def test_non_existent_version_returns_404():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/v3/health")
    assert response.status_code == 404
    assert "API Version v3 not found" in response.json()["detail"]

@pytest.mark.asyncio
async def test_accept_version_header_unsupported_returns_406():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/v1/health", headers={"Accept-Version": "v99"})
    assert response.status_code == 406
    assert "API version 'v99' is not supported" in response.json()["detail"]

@pytest.mark.asyncio
async def test_accept_version_header_supported_returns_200():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/v1/health", headers={"Accept-Version": "v1"})
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
