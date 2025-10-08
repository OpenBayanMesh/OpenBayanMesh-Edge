# Supported JSON Structures and Schema Mappings

This document outlines the expected JSON data structures for various domains and how schema mappings can be used to normalize or transform data during the import process.

## General JSON Structure

The importer script (`importer.py`) expects JSON data representing nodes and their potential relationships. The top-level JSON can be either a single object or an array of objects.

Each JSON object should ideally contain a unique identifier (e.g., `id`, `name`, or `uuid`) and a `domain` key. The value of the `domain` key will be used as the primary Neo4j label for the node.

### Node Properties

All key-value pairs in the JSON object (excluding `domain` and `connections`) will be imported as properties of the Neo4j node.

### Relationships

Relationships can be defined using a `connections` array within the JSON object. Each element in this array should be an object with the following keys:

*   `type`: The type of the relationship (e.g., `LOCATED_IN`, `HAS_SENSOR`).
*   `target_label`: The Neo4j label of the target node for the relationship.
*   `target_id`: The unique identifier of the target node. The importer will attempt to `MERGE` a relationship between the current node (identified by its `id`) and the target node.

## Example Domain: WEATHER

### Sample JSON Data (`schemas/weather_data.json`)

```json
[
  {
    "id": "weather-1",
    "domain": "WEATHER",
    "city": "Manila",
    "temperature": 30,
    "unit": "celsius",
    "timestamp": "2023-10-27T10:00:00Z",
    "connections": [
      {
        "type": "LOCATED_IN",
        "target_label": "CITY",
        "target_id": "manila-city-id"
      }
    ]
  },
  {
    "id": "weather-2",
    "domain": "WEATHER",
    "city": "Cebu",
    "temperature": 28,
    "unit": "celsius",
    "timestamp": "2023-10-27T11:00:00Z"
  }
]
```

### Sample Mapping File (`schemas/weather_mapping.json`)

This mapping file demonstrates renaming fields, converting types, and setting default values.

```json
{
  "rename_fields": {
    "city": "location_name",
    "temperature": "temp_celsius"
  },
  "type_conversions": {
    "temp_celsius": "float",
    "timestamp": "date"
  },
  "default_values": {
    "unit": "celsius"
  }
}
```

When importing `weather_data.json` with `weather_mapping.json`, the `city` field will be renamed to `location_name`, `temperature` to `temp_celsius` (and converted to a float), and `timestamp` will be converted to a date object. If `unit` is missing, it will default to `celsius`.

## Other Domains (Placeholders)

### HEALTH Domain

*   **JSON Structure**: (Example to be added)
*   **Schema Mapping**: (Example to be added)

### BUDGET Domain

*   **JSON Structure**: (Example to be added)
*   **Schema Mapping**: (Example to be added)

### MAPS Domain

*   **JSON Structure**: (Example to be added)
*   **Schema Mapping**: (Example to be added)
