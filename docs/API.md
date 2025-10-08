# API Documentation for OpenBayanMesh-Edge

This document provides comprehensive details about the OpenBayanMesh-Edge API, including available endpoints, data models, and versioning strategy.

## Auto-Generated OpenAPI Documentation
For an interactive and up-to-date view of all API endpoints, including request/response schemas, try the auto-generated documentation:

-   **Swagger UI:** Access at `/docs` (e.g., `http://localhost:8000/docs`)
-   **Redoc:** Access at `/redoc` (e.g., `http://localhost:8000/redoc`)

These interfaces reflect the current deployed code's API state and are the primary source for endpoint details.

## API Versioning
OpenBayanMesh-Edge implements a semantic API versioning scheme to manage changes and ensure stability. API versions are prefixed in the URL (e.g., `/v1/`).

-   **Active Versions:** Fully supported and maintained.
-   **Deprecated Versions:** Still available but no longer actively developed. Users are encouraged to migrate to newer versions. A sunset date will be announced.
-   **Upcoming Versions:** New versions under development, not yet stable for production use.

To see a list of all supported and deprecated API versions, along with their status and documentation links, access the `/versions` endpoint:

`GET /versions`

### Handling API Version Requests
-   If a non-existent or deprecated API version is requested, the API service will return `410 Gone` or `404 Not Found` with a descriptive message and a link to the latest documentation.
-   If a client sends an `Accept-Version` header with a non-supported version, the service will respond with `406 Not Acceptable` and a list of available versions.

## Data Domains

OpenBayanMesh-Edge nodes can specialize in providing data for specific domains (e.g., WEATHER, HEALTH, BUDGET, MAPS). A node advertises its supported data domains via the `/v1/info` endpoint. This allows clients to discover what kind of data a particular node can offer.

## API Endpoints (Version 1 - `/v1/`)

### System Status

#### `GET /v1/health`
Returns the health status of the API service.

-   **Response:**
    ```json
    {
      "status": "healthy",
      "timestamp": "2023-10-27T10:00:00.000000",
      "version": "v1"
    }
    ```

#### `GET /v1/info`
Returns general information about the API service, including supported data domains.

-   **Response:**
    ```json
    {
      "app_name": "OpenBayanMesh-Edge",
      "api_version": "v1",
      "python_version": "3.12.x",
      "data_domains": [
        "WEATHER",
        "HEALTH"
      ]
    }
    ```

#### `GET /v1/metrics`
(Optional Feature) Returns metrics about the API service.

-   **Response:**
    ```json
    {
      "message": "Metrics endpoint for v1",
      "metrics": {}
    }
    ```

### Data Operations

#### `GET /v1/query`
Placeholder for general data querying operations.

-   **Response:**
    ```json
    {
      "message": "Query endpoint for v1",
      "data": []
    }
    ```

#### `GET /v1/node/{node_id}`
Retrieves a Neo4j node by its internal ID.

-   **Parameters:**
    -   `node_id` (integer, path): The internal ID of the Neo4j node.

-   **Response (200 OK):**
    ```json
    {
      "id": 123,
      "labels": [
        "MeshNode",
        "Device"
      ],
      "properties": {
        "name": "Router-1",
        "location": "Office A"
      }
    }
    ```

-   **Error Response (404 Not Found):**
    ```json
    {
      "detail": "Node not found"
    }
    ```

## Changelog & Migration Guides
(To be added in future releases)

For major releases, a `CHANGELOG.md` will clearly describe all breaking changes, new features, and deprecated endpoints. Migration guides will be provided for upgrading between major API versions.
