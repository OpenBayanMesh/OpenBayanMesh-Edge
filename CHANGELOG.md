# Changelog

## Version 1.0.0 (YYYY-MM-DD)

### Importer Script (`src/importer.py`)

*   Initial implementation of the Neo4j data import tool.
*   Supports importing JSON data (single object or array of objects) into Neo4j.
*   Dynamic node creation with labels based on `domain` key and properties from JSON fields.
*   Support for defining and importing relationships via a `connections` array in JSON.
*   Implemented `--merge` flag for idempotent (upsert) imports.
*   Introduced `--batch-size` for efficient processing of large datasets.
*   Added `--mapping-file` for custom field renaming, type conversions, and default values.
*   Comprehensive logging and summary reporting for import operations.
*   Implemented transaction rollback for atomicity of batch imports.
*   Enhanced error handling for Neo4j connection, JSON parsing, and data validation.

### Dynamic Domain API Layer (`src/main.py`, `src/routers/v1.py`, `src/domain_manager.py`)

*   Created `src/domain_manager.py` for dynamic management and caching of domain schemas.
*   Enhanced `/v1/info` endpoint to list all supported domains with their inferred properties and relationships.
*   Implemented dynamic `/v1/query/{domain}` endpoint for querying nodes with filtering capabilities.
*   Implemented dynamic `/v1/query/{domain}/relationships` endpoint for querying relationships with filtering capabilities.
*   Added validation for domain existence, property presence, and basic type matching in query endpoints.
*   Implemented error handling for unsupported domains, invalid queries, and deprecated domains.
*   Introduced admin endpoints (`/v1/admin/refresh-schemas`, `/v1/admin/deprecate-domain/{domain_name}`) for schema management.

### Documentation (`docs/`)

*   Created `docs/importer_guide.md` for detailed usage of the import script.
*   Created `docs/json_structures.md` explaining supported JSON formats and schema mapping examples.
*   Created `docs/extending_domains.md` with instructions on how to add new data domains.
*   Created `docs/api_queries.md` with examples for querying the dynamic API endpoints.

