# Importer Script User Guide

This guide provides instructions on how to use the `importer.py` script to import JSON data into the Neo4j database.

## Usage

To run the importer script, navigate to the root directory of the project and execute the script using Python:

```bash
python src/importer.py <path_to_json_file> --domain <DOMAIN_TYPE> [OPTIONS]
```

### Arguments

*   `<path_to_json_file>`: **Required**. The absolute or relative path to the JSON data file you want to import. The file can contain a single JSON object or an array of JSON objects.

### Required Options

*   `--domain <DOMAIN_TYPE>`: **Required**. Specifies the domain type for the data being imported (e.g., `WEATHER`, `HEALTH`, `BUDGET`, `MAPS`). This will be used as the primary label for nodes created in Neo4j.

### Optional Options

*   `--uri <NEO4J_URI>`: The Neo4j connection URI. Defaults to the `NEO4J_URI` environment variable.
*   `--user <NEO4J_USER>`: The Neo4j username. Defaults to the `NEO4J_USER` environment variable.
*   `--password <NEO4J_PASSWORD>`: The Neo4j password. Defaults to the `NEO4J_PASSWORD` environment variable.
*   `--merge`: Use `MERGE` (upsert) logic instead of `CREATE` for conflicting records. If a node with the same `id` property already exists, its properties will be updated; otherwise, a new node will be created.
*   `--batch-size <SIZE>`: Number of records to process in each batch (default: `1000`). Adjust this value based on your system's memory and Neo4j's performance to optimize import speed.
*   `--mapping-file <path_to_mapping_file>`: Path to a JSON file defining custom mappings and schema normalization rules. See [Extending to New Domains](extending_domains.md) for details on the mapping file format.

## Environment Variables

The script relies on the following environment variables for Neo4j connection details. It is recommended to set these in a `.env` file in the project root.

*   `NEO4J_URI`: Neo4j database URI (e.g., `bolt://localhost:7687`)
*   `NEO4J_USER`: Neo4j database username
*   `NEO4J_PASSWORD`: Neo4j database password

## JSON Data Format

The importer supports JSON files containing either a single JSON object or an array of JSON objects. Each object represents a node to be imported into Neo4j.

### Example Single Object JSON

```json
{
  "id": "unique-id-1",
  "domain": "WEATHER",
  "city": "Manila",
  "temperature": 30,
  "unit": "celsius",
  "timestamp": "2023-10-27T10:00:00Z"
}
```

### Example Array of Objects JSON

```json
[
  {
    "id": "unique-id-1",
    "domain": "WEATHER",
    "city": "Manila",
    "temperature": 30,
    "unit": "celsius",
    "timestamp": "2023-10-27T10:00:00Z"
  },
  {
    "id": "unique-id-2",
    "domain": "WEATHER",
    "city": "Cebu",
    "temperature": 28,
    "unit": "celsius",
    "timestamp": "2023-10-27T11:00:00Z"
  }
]
```

### Relationships

Relationships can be defined within the JSON object using a `connections` array. Each object in the `connections` array should specify the `type` of the relationship, the `target_label` of the connected node, and the `target_id` of the connected node.

```json
{
  "id": "weather-1",
  "domain": "WEATHER",
  "city": "Manila",
  "connections": [
    {
      "type": "LOCATED_IN",
      "target_label": "CITY",
      "target_id": "manila-city-id"
    }
  ]
}
```

## Troubleshooting

*   **Neo4j Connection Errors**: Ensure Neo4j is running and accessible from where you are running the script. Verify `NEO4J_URI`, `NEO4J_USER`, and `NEO4J_PASSWORD` are correctly set in your `.env` file or via CLI arguments.
*   **Malformed JSON**: The script will report an error if the JSON file is not valid. Use a JSON linter to check your file.
*   **Missing Identifiers**: For `MERGE` operations, records should ideally have an `id` property. If not present, the script will log a warning.
*   **Transaction Rollback**: If an error occurs during the processing of a batch, the entire batch will be rolled back to maintain data integrity. Check the logs for specific error messages.

## Summary Report

Upon completion, the script will output a summary report to the console, indicating the number of successful and failed imports.
