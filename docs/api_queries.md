# API Query Examples

This guide provides examples of how to query the OpenBayanMesh-Edge API for nodes and relationships across different domains.

## Base URL

All API endpoints are prefixed with `/v1`. Assuming your API is running locally on port `8000`, the base URL would be `http://localhost:8000/v1`.

## 1. Get API Information (`/v1/info`)

This endpoint provides information about the API, including all supported data domains and their inferred schemas (properties and relationships).

```bash
curl http://localhost:8000/v1/info
```

**Example Response (partial)**:

```json
{
  "app_name": "OpenBayanMesh-Edge",
  "api_version": "v1",
  "supported_domains": {
    "WEATHER": {
      "properties": {
        "id": "str",
        "location_name": "str",
        "temp_celsius": "float",
        "unit": "str",
        "timestamp": "date"
      },
      "relationships": [
        {
          "type": "LOCATED_IN",
          "target_label": "CITY"
        }
      ]
    },
    "INVENTORY": {
      "properties": {
        "id": "str",
        "name": "str",
        "quantity": "int",
        "status": "str"
      },
      "relationships": [
        {
          "type": "MANUFACTURED_BY",
          "target_label": "COMPANY"
        }
      ]
    }
  }
}
```

## 2. Query Nodes by Domain (`/v1/query/{domain}`)

This endpoint allows you to query nodes within a specific domain, optionally filtering by node properties.

### Query all nodes in a domain

```bash
curl http://localhost:8000/v1/query/WEATHER
```

### Query nodes with filters

Filter by one or more properties using the `properties` query parameter. Properties should be in `key=value` format, separated by commas.

**Example: Get weather records for Manila with temperature 30**

```bash
curl "http://localhost:8000/v1/query/WEATHER?properties=location_name=Manila,temp_celsius=30.0"
```

**Example: Get inventory items with quantity greater than 50 (assuming `quantity` is an integer)**

```bash
curl "http://localhost:8000/v1/query/INVENTORY?properties=quantity=50"
```

### Handling Deprecated Domains

If you query a deprecated domain, the API will return an error message indicating its deprecation status.

```bash
curl http://localhost:8000/v1/query/DEPRECATED_DOMAIN
```

## 3. Query Relationships by Domain (`/v1/query/{domain}/relationships`)

This endpoint allows you to query relationships originating from nodes within a specific domain, optionally filtering by relationship type or target node label.

### Query all relationships from a domain

```bash
curl http://localhost:8000/v1/query/WEATHER/relationships
```

### Query relationships with filters

**Example: Get `LOCATED_IN` relationships from WEATHER nodes to CITY nodes**

```bash
curl "http://localhost:8000/v1/query/WEATHER/relationships?rel_type=LOCATED_IN&target_label=CITY"
```

**Example: Get relationships with a specific property (e.g., `since=2023`)**

```bash
curl "http://localhost:8000/v1/query/INVENTORY/relationships?properties=since=2023"
```

## 4. Admin Endpoints (Requires Authentication/Authorization in Production)

These endpoints are for administrative purposes and should be protected in a production environment.

### Refresh Domain Schemas (`/v1/admin/refresh-schemas`)

Triggers a refresh of all domain schemas. Useful after new data has been imported via `importer.py`.

```bash
curl -X POST http://localhost:8000/v1/admin/refresh-schemas
```

### Deprecate a Domain (`/v1/admin/deprecate-domain/{domain_name}`)

Marks a domain as deprecated, optionally providing a sunset date.

**Example: Deprecate the `OLD_DATA` domain with a sunset date**

```bash
curl -X POST "http://localhost:8000/v1/admin/deprecate-domain/OLD_DATA?sunset_date=2025-12-31"
```

**Example: Deprecate the `TEST_DOMAIN` domain without a sunset date**

```bash
curl -X POST http://localhost:8000/v1/admin/deprecate-domain/TEST_DOMAIN
```
