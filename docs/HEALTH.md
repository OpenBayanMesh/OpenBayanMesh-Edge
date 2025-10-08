# Health Endpoint (`/health`) Explanation and Troubleshooting

This document provides details about the `/health` endpoint in the OpenBayanMesh-Edge API and offers guidance for troubleshooting common issues.

## Purpose of the `/health` Endpoint
The `/health` endpoint is a critical component for monitoring the operational status of the OpenBayanMesh-Edge API service. It provides a quick and programmatic way to determine if the application is running, responsive, and able to serve requests.

Monitoring systems, load balancers, and container orchestrators (like Docker Compose, Kubernetes) typically use this endpoint to perform health checks. If the endpoint returns a successful status (e.g., HTTP 200 OK), the service is considered healthy. Any other status code (e.g., 5xx errors) indicates a problem.

## Endpoint Details

-   **Path:** `/v1/health` (and similar paths for other API versions, e.g., `/v2/health` if available)
-   **Method:** `GET`
-   **Authentication:** Not required.

### Expected Response
A successful response from the `/health` endpoint will typically look like this:

```json
{
  "status": "healthy",
  "timestamp": "2023-10-27T10:00:00.000000",
  "version": "v1"
}
```

-   `status`: Indicates the overall health of the service. Expected value is `"healthy"`.
-   `timestamp`: The exact time the health check was performed, in ISO 8601 format.
-   `version`: The API version of the endpoint being checked.

## Troubleshooting the `/health` Endpoint
If the `/health` endpoint is not returning a `200 OK` status or the expected `"status": "healthy"` payload, consider the following troubleshooting steps:

### 1. Check Docker Container Status
Ensure all relevant Docker containers are running:

```bash
docker-compose ps
```

Look for `Up` status for `fastapi_app`, `neo4j`, and `cloudflared`. If any are not `Up`, investigate their logs.

### 2. Review Container Logs
Check the logs of the `fastapi_app` service for any errors or exceptions:

```bash
docker-compose logs fastapi_app
```

If you suspect issues with other services affecting the API, check their logs as well:

```bash
docker-compose logs neo4j
docker-compose logs cloudflared
```

Look for error messages, stack traces, or warnings that might indicate why the application is not starting or responding correctly.

### 3. Verify Network Connectivity
Ensure the FastAPI application is accessible within the Docker network and from your host machine:

-   **From Host:** Try to access `http://localhost:8000/v1/health` directly from your browser or using `curl`.
    ```bash
    curl http://localhost:8000/v1/health
    ```
-   **Within Docker Network:** If you have other services that depend on `fastapi_app`, ensure they can reach it at `http://fastapi_app:8000`.

### 4. Check Environment Variables
Incorrect or missing environment variables can prevent the application from starting or functioning correctly. Verify your `.env` file and ensure all necessary variables are set as per `.env.example`.

### 5. FastAPI Application Issues
-   **Syntax Errors:** Check the `fastapi_app` logs for Python syntax errors or unhandled exceptions during startup.
-   **Dependencies:** Ensure all Python dependencies listed in `src/requirements.txt` are correctly installed within the container. Rebuild the `fastapi_app` service if you've changed `requirements.txt`:
    ```bash
    docker-compose up --build -d fastapi_app
    ```

### 6. Neo4j Connectivity Issues
If the `/health` endpoint (or other API endpoints) attempts to connect to Neo4j and fails, check the `neo4j` container logs. Ensure the Neo4j database is running and accessible with the provided credentials.

### 7. Cloudflared Tunnel Issues
If you are accessing the API via the Cloudflare Tunnel and encounter issues, check the `cloudflared` container logs. Ensure the tunnel is connected to Cloudflare and correctly routing traffic to the `fastapi_app` service.

By systematically checking these areas, you should be able to diagnose and resolve most issues preventing the `/health` endpoint from reporting a healthy status.