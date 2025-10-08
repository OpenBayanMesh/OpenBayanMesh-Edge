# OpenBayanMesh-Edge

## Introduction
OpenBayanMesh-Edge is a robust and scalable edge service built with FastAPI (Python 3.12 LTS), Neo4j, and Cloudflared. It provides a secure and versioned API for interacting with mesh network data, designed for high availability and easy deployment using Docker Compose.

## Architectural Overview
The OpenBayanMesh-Edge stack consists of:
- **FastAPI Web Service:** A Python 3.12 LTS application providing a versioned REST API.
- **Neo4j Database:** A graph database for storing and querying mesh network data.
- **Cloudflared Tunnel:** A secure tunnel for exposing the API to the internet via Cloudflare Zero Trust.

## Main Features
- **API Versioning:** Supports semantic versioning for API endpoints (e.g., `/v1/`, `/v2/`).
- **Containerized Deployment:** Easy setup and deployment using Docker Compose.
- **Secure Access:** Integration with Cloudflare Zero Trust for secure external access.
- **Graph Database:** Utilizes Neo4j for efficient storage and querying of interconnected data.
- **Comprehensive Documentation:** Auto-generated OpenAPI docs and extended markdown documentation.

## API Versioning Explanation
OpenBayanMesh-Edge employs a semantic versioning scheme for its API to ensure backward compatibility and clear communication of changes. New features or non-breaking changes are typically introduced within the same major version. Breaking changes will result in a new major API version (e.g., `/v2/`), with previous versions remaining available for a defined sunset period. The `/versions` endpoint provides a list of all supported and deprecated API versions.

## Project Structure

The project follows a standard Python project layout:

```
.
├── .env.example
├── .flake8
├── .gitignore
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── docker-compose.yml
├── Dockerfile
├── LICENSE.md
├── mypy.ini
├── README.md
├── requirements.txt
├── cloudflared/
│   └── config.yaml
├── docs/
│   └── ...
├── scripts/
│   ├── init_db.sh
│   └── test.sh
├── src/
│   ├── __init__.py
│   ├── dependencies.py
│   ├── domain_manager.py
│   ├── importer.py
│   ├── main.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── weather_data.json
│   │   └── weather_mapping.json
│   └── routers/
│       ├── __init__.py
│       └── v1.py
└── tests/
    ├── __init__.py
    ├── test_api_v1.py
    └── test_versioning.py
```

## Quickstart

### Prerequisites
- Docker and Docker Compose installed.
- A Cloudflare Zero Trust account and a tunnel token (`TUNNEL_TOKEN`).
- (Optional) A Cloudflare Tunnel ID (`TUNNEL_ID`) if you have an existing tunnel.

### 1. Clone the repository
```bash
git clone https://github.com/your-org/OpenBayanMesh-Edge.git
cd OpenBayanMesh-Edge
```

### 2. Configure Environment Variables
Copy the example environment file and fill in your details:
```bash
cp .env.example .env
# Open .env and fill in TUNNEL_TOKEN, TUNNEL_ID, DATA_DOMAINS (e.g., WEATHER,HEALTH), REGION (e.g., PH-NCR), and any other desired configurations.
```

### 3. Build and Run with Docker Compose
```bash
docker-compose up --build -d
```
This will start the FastAPI application, Neo4j database, and Cloudflared tunnel.

### 4. Access the API
- **Local API:** `http://localhost:8000`
- **API Documentation (Swagger UI):** `http://localhost:8000/docs`
- **API Documentation (Redoc):** `http://localhost:8000/redoc`
- **Cloudflare Tunnel:** Once Cloudflared is configured and running, your API will be accessible via your configured Cloudflare domain.

## Further Documentation
Refer to the `docs/` directory for more detailed information:
- `docs/INSTALL.md`: Detailed installation guide.
- `docs/API.md`: Comprehensive API documentation.
- `docs/HEALTH.md`: Explanation of the health endpoint and troubleshooting.
- `docs/SECURITY.md`: Security guidelines.
- `docs/VERSIONING.md`: In-depth explanation of API versioning.
- `scripts/init_db.sh`: Script for initializing the Neo4j database.
- `scripts/test.sh`: Script for running tests.