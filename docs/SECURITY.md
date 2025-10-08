# Security Guidelines for OpenBayanMesh-Edge

This document outlines essential security guidelines for contributors and deployers of the OpenBayanMesh-Edge project. Adhering to these practices helps maintain the integrity, confidentiality, and availability of the system.

## General Security Principles

-   **Least Privilege:** Services and users should operate with the minimum necessary permissions to perform their functions.
-   **Defense in Depth:** Employ multiple layers of security controls to protect against various threats.
-   **Secure by Design:** Integrate security considerations from the initial design phase through deployment.
-   **Regular Updates:** Keep all software components (OS, Docker, libraries, dependencies) up-to-date to patch known vulnerabilities.

## Docker and Docker Compose Security

1.  **Image Security:**
    -   Use official and trusted Docker images (e.g., `python:3.12-slim-bookworm`, `neo4j:latest`, `cloudflare/cloudflared:latest`).
    -   Avoid using images from unknown sources.
    -   Regularly scan Docker images for vulnerabilities using tools like Trivy or Clair.

2.  **Container User:**
    -   Run containers as non-root users whenever possible. The `Dockerfile` for `fastapi_app` specifies a non-root user (`appuser`). Official Neo4j and Cloudflared images also run as non-root users by default.
    -   The `docker-compose.yml` should enable default seccomp and user namespace features for enhanced isolation (Docker Compose applies a default seccomp profile automatically).

3.  **Resource Limits:**
    -   Implement resource limits (CPU, memory) for containers in `docker-compose.yml` to prevent resource exhaustion attacks.

4.  **Network Isolation:**
    -   The Docker Compose network (`openbayanmesh-network`) is configured to isolate internal traffic. Only explicitly exposed ports should be accessible externally.
    -   Avoid exposing unnecessary ports from containers to the host machine.

5.  **Volume Permissions:**
    -   Ensure that mounted volumes have appropriate permissions to prevent unauthorized access to data.

## FastAPI API Security

1.  **Input Validation and Sanitization:**
    -   All API inputs must be rigorously validated and sanitized using Pydantic models to prevent common vulnerabilities like injection attacks (SQL, NoSQL, XSS).
    -   Use parameterized queries for all database interactions (e.g., with Neo4j) to prevent Cypher/SQL injection.

2.  **Error Handling:**
    -   Error responses should be generic and avoid surfacing sensitive diagnostic details, stack traces, or internal data structures to clients.

3.  **CORS Configuration:**
    -   Restrict CORS origins (`CORS_ALLOWED_ORIGINS`) to only those domains that are explicitly allowed to access your API. Avoid using `*` in production unless absolutely necessary and understood.

4.  **Rate Limiting:**
    -   Implement API rate limiting (`RATE_LIMIT_ENABLED`, `RATE_LIMIT_PER_MINUTE`) to protect against brute-force attacks and denial-of-service (DoS) attempts. For production, consider a more robust solution than the in-memory placeholder.

5.  **Authentication and Authorization (Future):**
    -   If authentication is implemented, use secure methods (e.g., OAuth2, JWT) and ensure proper authorization checks are performed on all protected endpoints.

6.  **Secrets Management:**
    -   Never commit API keys, database credentials, or other sensitive information directly into source control. Use environment variables (via `.env` file) or a dedicated secrets management solution.
    -   **Blocking Sensitive Configurations:** The system is designed to prevent committing sensitive credentials. Node operators must ensure their `.env` and `cloudflared/config.yaml` do not expose sensitive data. Maintainers will notify and assist node owners if such configurations are detected.

## Cloudflared Tunnel Security

1.  **Tunnel Token Security:**
    -   Your `TUNNEL_TOKEN` is highly sensitive. Treat it like a password. Never commit it to source control. Store it securely in your `.env` file.

2.  **Ingress Rules:**
    -   Configure `cloudflared/config.yaml` with precise ingress rules. Only expose the necessary API endpoints and services. Avoid broad `service: http_status:200` rules unless specifically required and secured by Cloudflare Access policies.

3.  **Cloudflare Zero Trust Policies:**
    -   Leverage Cloudflare Zero Trust Access policies to add additional layers of authentication and authorization before requests even reach your origin server.

## Neo4j Database Security

1.  **Strong Passwords:**
    -   Use strong, unique passwords for the Neo4j database (`NEO4J_PASSWORD`). Change default credentials immediately.

2.  **Least Privilege:**
    -   Configure Neo4j users with the minimum necessary roles and permissions. The API should connect with a user that only has the required read/write access.

3.  **Query Injection Prevention:**
    -   Always use parameterized queries when interacting with Neo4j from the FastAPI application to prevent Cypher injection attacks.

4.  **Data Encryption:**
    -   Ensure data at rest (on the volume) and data in transit (between FastAPI and Neo4j) are encrypted. Neo4j typically uses Bolt+SSL for encrypted connections.

## Code Security

1.  **Dependency Scanning:**
    -   Regularly scan your project dependencies (`requirements.txt`) for known vulnerabilities using tools like `Safety` and `Bandit`. These scans are integrated into the CI/CD pipeline.

2.  **Static Analysis:**
    -   Use static code analysis tools (linters, type checkers) to identify potential security flaws and maintain code quality.

## Vulnerability Management and Response

1.  **Reporting Vulnerabilities:**
    -   If you discover a security vulnerability in OpenBayanMesh-Edge, please report it privately and securely to the maintainers by emailing [security@openbayanmesh.org](mailto:security@openbayanmesh.org) (replace with actual email). Do not open a public GitHub issue.
    -   Provide a detailed description of the vulnerability, steps to reproduce, and potential impact.

2.  **Security Advisories:**
    -   When a new security vulnerability is discovered and confirmed, the repository will issue a security advisory (e.g., via GitHub Security Advisories) and update guidance in this `SECURITY.md` file.

3.  **Prioritizing Hotfixes and Patch Releases:**
    -   Critical security issues will be prioritized for hotfixes and coordinated patch releases with the community to ensure rapid deployment of remediations.

4.  **Contributor Notification and Remediation:**
    -   When security issues are found during code review or automated scanning, contributors will be notified and provided with recommended remediations to address the vulnerabilities.

By following these guidelines, we can collectively build and maintain a secure OpenBayanMesh-Edge system.
