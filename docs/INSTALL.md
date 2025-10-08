# Installation Guide for OpenBayanMesh-Edge

This document provides detailed, step-by-step instructions for deploying and running the OpenBayanMesh-Edge services using Docker Compose.

## Prerequisites
Before you begin, ensure you have the following installed on your system:

1.  **Docker:** [Install Docker Engine](https://docs.docker.com/engine/install/) for your operating system.
2.  **Docker Compose:** [Install Docker Compose](https://docs.docker.com/compose/install/) (usually comes with Docker Desktop).
3.  **Git:** [Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).
4.  **Cloudflare Zero Trust Account:** You will need an active Cloudflare Zero Trust account to set up the Cloudflared tunnel. Obtain your `TUNNEL_TOKEN` and optionally `TUNNEL_ID` from your Cloudflare dashboard.

## Step-by-Step Installation

### 1. Clone the Repository
First, clone the OpenBayanMesh-Edge repository to your local machine:

```bash
git clone https://github.com/your-org/OpenBayanMesh-Edge.git
cd OpenBayanMesh-Edge
```

### 2. Configure Environment Variables
The project uses environment variables for configuration. A template file `.env.example` is provided.

Copy this file to `.env` in the root directory of the project:

```bash
cp .env.example .env
```

Now, open the newly created `.env` file with your preferred text editor and update the variables:

-   **`TUNNEL_TOKEN`**: **Required.** Your Cloudflare Tunnel token. You can generate this from your Cloudflare Zero Trust dashboard under `Access -> Tunnels`.
-   **`TUNNEL_ID`**: **Required.** The UUID of your Cloudflare Tunnel. This is also found in your Cloudflare Zero Trust dashboard. If you don't have one, Cloudflared will create one for you, but it's best to pre-configure it.
-   **`NEO4J_PASSWORD`**: Change `password` to a strong, secure password for your Neo4j database.
-   **`CORS_ALLOWED_ORIGINS`**: If you need to restrict CORS, specify a comma-separated list of allowed origins (e.g., `http://localhost:3000,https://yourdomain.com`). Use `*` for all origins (default).
-   **`REGION`**: Your node's geographical region (e.g., `PH-NCR`). Refer to [`docs/PHILIPPINE_REGIONS.md`](PHILIPPINE_REGIONS.md) for the naming convention.
-   **`DATA_DOMAINS`**: A comma-separated list of data domains this node will serve (e.g., `WEATHER,HEALTH,BUDGET`).
-   Review other variables like `LOG_LEVEL`, `RATE_LIMIT_ENABLED`, `RATE_LIMIT_PER_MINUTE`, `APP_ENV`, `DEFAULT_API_VERSION`, and adjust them as needed.

### 3. Build and Run the Services
Once your `.env` file is configured, you can build and start all services using Docker Compose:

```bash
docker-compose up --build -d
```

-   `--build`: This flag ensures that Docker images are rebuilt. It's important to use this the first time or after changing `Dockerfile` or `requirements.txt`.
-   `-d`: This flag runs the containers in detached mode (in the background).

### 4. Verify Service Status

To check if all services are running correctly, use:

```bash
docker-compose ps
```

You should see `Up` status for `fastapi_app`, `neo4j`, and `cloudflared`.

To view logs for all services:

```bash
docker-compose logs -f
```

### 5. Access the API

-   **Local FastAPI Application:** The FastAPI service will be accessible locally at `http://localhost:8000`.
-   **API Documentation (Swagger UI):** Access the interactive API documentation at `http://localhost:8000/docs`.
-   **API Documentation (Redoc):** Access the Redoc documentation at `http://localhost:8000/redoc`.
-   **Cloudflare Tunnel Access:** Once your Cloudflare Tunnel is fully set up and connected, your API will be accessible via the hostname you configured in your `cloudflared/config.yaml` (e.g., `https://your-domain.com`).

### 6. Stopping the Services

To stop all running services and remove their containers, networks, and volumes (except named volumes like `neo4j_data`):

```bash
docker-compose down
```

To stop and remove named volumes as well (use with caution, as this will delete your Neo4j data):

```bash
docker-compose down --volumes
```