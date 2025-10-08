from fastapi import FastAPI, HTTPException, Request, status, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Dict, Any
import os
import logging
import time
from collections import defaultdict
import re # Import re module

from src.routers import v1

# --- Configuration from Environment Variables ---
DEFAULT_API_VERSION = os.getenv("DEFAULT_API_VERSION", "v1")
CORS_ENABLED = os.getenv("CORS_ENABLED", "true").lower() == "true"
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "*").split(",")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "false").lower() == "true"
RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
TELEMETRY_ENABLED = os.getenv("TELEMETRY_ENABLED", "false").lower() == "true" # New telemetry flag

# --- Global Error Counter ---
fatal_error_count = 0

# --- Logging Setup ---
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SensitiveDataFilter(logging.Filter):
    def filter(self, record):
        # Redact sensitive environment variables
        if hasattr(record, 'msg') and isinstance(record.msg, str):
            record.msg = record.msg.replace(os.getenv("NEO4J_PASSWORD", "password"), "********")
            record.msg = record.msg.replace(os.getenv("TUNNEL_TOKEN", "your_cloudflare_tunnel_token_here"), "********")
        
        # Attempt to redact IP addresses from the message itself if present
        if hasattr(record, 'msg') and isinstance(record.msg, str):
            # Simple regex to find common IPv4 patterns
            record.msg = re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '[REDACTED_IP]', record.msg)

        return True

logger.addFilter(SensitiveDataFilter())

app = FastAPI(
    title="OpenBayanMesh-Edge API",
    description="API for OpenBayanMesh-Edge services, supporting versioning.",
    version="1.0.0", # This will be dynamically updated with versioning
)

# --- CORS Middleware ---
if CORS_ENABLED:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info(f"CORS enabled for origins: {CORS_ALLOWED_ORIGINS}")
else:
    logger.info("CORS is disabled.")

# --- Rate Limiting (Placeholder) ---
# In a production environment, consider using a dedicated rate limiting library
# like `fastapi-limiter` or a reverse proxy (e.g., Nginx, Cloudflare).
# This is a very basic in-memory implementation and not suitable for production.
if RATE_LIMIT_ENABLED:
    request_counts = defaultdict(lambda: defaultdict(int))
    last_reset_time = defaultdict(float)

    async def rate_limiter(request: Request):
        client_ip = request.client.host
        current_time = time.time()

        if current_time - last_reset_time[client_ip] > 60:
            request_counts[client_ip]["count"] = 0
            last_reset_time[client_ip] = current_time

        request_counts[client_ip]["count"] += 1

        if request_counts[client_ip]["count"] > RATE_LIMIT_PER_MINUTE:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")

    app.dependency_overrides[Depends(rate_limiter)] = rate_limiter
    logger.info(f"Rate limiting enabled: {RATE_LIMIT_PER_MINUTE} requests per minute.")
else:
    logger.info("Rate limiting is disabled.")

# Mount API version 1 router
app.include_router(v1.router, prefix="/v1")

# Placeholder for future API versions
# app.include_router(v2.router, prefix="/v2")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": f"Welcome to OpenBayanMesh-Edge API. Access /{DEFAULT_API_VERSION}/ for the current API version."}

@app.get("/versions", tags=["API Versioning"])
async def get_api_versions():
    # This should dynamically list available versions based on mounted routers
    # For now, hardcode v1 and a deprecated v2 for demonstration
    return {
        "versions": [
            {"version": "v1", "status": "active", "documentation_url": "/docs#/v1"},
            {"version": "v2", "status": "deprecated", "documentation_url": "/docs#/v2", "sunset_date": "2025-12-31"},
        ]
    }

# Deprecated endpoint example: v2/health
@app.get("/v2/health", tags=["v2 - System Status"], deprecated=True)
async def health_v2_deprecated(response: Response):
    response.headers["Warning"] = "299 - \"API Version v2 is deprecated and will be removed after 2025-12-31. Please migrate to v1 or newer.\""
    return {"status": "healthy", "timestamp": datetime.now().isoformat(), "version": "v2", "message": "This endpoint is deprecated."}

# Error handling for non-existent or deprecated API versions
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    global fatal_error_count
    if exc.status_code >= 500:
        fatal_error_count += 1
        logger.error(f"Fatal error: {exc.detail} at {request.url}", exc_info=True)

    if exc.status_code == status.HTTP_404_NOT_FOUND:
        path_parts = request.url.path.split('/')
        if len(path_parts) > 1 and path_parts[1].startswith('v') and path_parts[1][1:].isdigit():
            version_requested = path_parts[1]
            # In a real scenario, check against a list of active/deprecated versions
            if version_requested == "v2": # Example of a non-existent version
                # This case is now handled by the specific @app.get("/v2/health") above
                # If a different v2 endpoint is requested and not found, it will fall through to generic 404
                pass
            elif version_requested == "v3": # Example of a non-existent version
                return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                     detail=f"API Version {version_requested} not found. See /versions for available API versions.",
                                     headers={"Link": "</versions>; rel=\"versions\""})
    return exc

# Generic catch-all for unmatched routes (after all other routes are checked)
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def catch_all(path: str):
    # This will only be hit if no other route matches, including versioned ones.
    # The HTTPException handler above will catch version-specific 404s.
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Endpoint not found.")