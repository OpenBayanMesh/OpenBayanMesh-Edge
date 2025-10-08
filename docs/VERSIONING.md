# API Versioning in OpenBayanMesh-Edge

This document details the rationale, implementation, and usage of API versioning within the OpenBayanMesh-Edge project.

## Rationale for API Versioning
API versioning is crucial for evolving an API while maintaining compatibility with existing clients. It allows for:

-   **Backward Compatibility:** Introducing new features or making non-breaking changes without affecting older clients.
-   **Clear Communication:** Explicitly signaling breaking changes to consumers, giving them time to adapt.
-   **Controlled Evolution:** Managing the lifecycle of API features, including deprecation and eventual removal.
-   **Reduced Risk:** Minimizing the risk of breaking existing integrations when deploying updates.

## Versioning Scheme: URI Path Versioning
OpenBayanMesh-Edge uses **URI Path Versioning**, where the API version is included as a prefix in the URL path (e.g., `/v1/resource`, `/v2/resource`).

### Examples:
-   `GET /v1/health`: Accesses the health endpoint of API version 1.
-   `GET /v2/users`: Would access the users endpoint of API version 2 (if implemented).

## API Version Lifecycle

1.  **Active:** The current, fully supported, and actively maintained version(s) of the API. New features and bug fixes are applied to active versions.
2.  **Deprecated:** A version that is still available but no longer actively developed. Clients are strongly encouraged to migrate to a newer active version. A sunset date will be announced, after which the version will be removed.
3.  **Sunset/Removed:** A version that has been taken offline and is no longer accessible.

## Managing API Versions

### Listing Available Versions
You can query the `/versions` endpoint to get a list of all supported and deprecated API versions, along with their status and documentation links:

`GET /versions`

**Example Response:**
```json
{
  "versions": [
    {
      "version": "v1",
      "status": "active",
      "documentation_url": "/docs#/v1"
    },
    {
      "version": "v2",
      "status": "deprecated",
      "documentation_url": "/docs#/v2",
      "sunset_date": "2025-12-31"
    }
  ]
}
```

### Requesting Specific Versions
Clients should explicitly request the desired API version by including it in the URL path (e.g., `/v1/health`).

### Handling Non-Existent or Deprecated Versions
-   If a client requests a non-existent API version (e.g., `/v3/health` when only `v1` and `v2` exist), the API will respond with `404 Not Found` and a message guiding the client to the `/versions` endpoint.
-   If a client requests a deprecated API version (e.g., `/v2/health` after its sunset date or if explicitly marked as `410 Gone`), the API will respond with `410 Gone` and a message indicating deprecation, along with a link to the `/versions` endpoint.

### `Accept-Version` Header
While URI path versioning is the primary method, the API also supports an `Accept-Version` header for explicit version negotiation. If this header is present and specifies a version not supported by the requested endpoint, the API will respond with `406 Not Acceptable`.

**Example Request with `Accept-Version` header:**

```
GET /v1/health
Accept-Version: v1
```

## Upgrade and Migration Guide
(To be developed as new API versions are introduced)

When a new major API version is released, a detailed migration guide will be provided in `docs/API.md` and linked from the `/versions` endpoint. This guide will outline:

-   All breaking changes.
-   New features and enhancements.
-   Recommended steps for migrating client applications from older versions to the new one.
-   Any changes in data models, authentication, or error handling.

By understanding and utilizing the API versioning strategy, developers can build robust and future-proof integrations with OpenBayanMesh-Edge.