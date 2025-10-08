# Extending to New Domains

This guide explains how to extend the OpenBayanMesh-Edge system to support new data domains. This involves defining your JSON data structure, optionally creating a mapping file for normalization, and then importing your data using the `importer.py` script.

## 1. Define Your JSON Data Structure

Each new domain requires a clear JSON structure for its data. This structure will be used by the `importer.py` script to create nodes and relationships in Neo4j.

### Key Considerations:

*   **Unique Identifier**: Each record should have a unique identifier (e.g., `id`, `name`, `uuid`). This is crucial for `MERGE` operations and for establishing relationships.
*   **`domain` Field**: Include a `"domain": "YOUR_DOMAIN_NAME"` field in each JSON object. This value will be used as the primary label for the nodes in Neo4j.
*   **Properties**: All other key-value pairs in your JSON object will become properties of the Neo4j node.
*   **Relationships**: If your data includes relationships to other nodes, define them using a `connections` array. Each connection object should have:
    *   `"type"`: The type of the relationship (e.g., `HAS_PART`, `BELONGS_TO`).
    *   `"target_label"`: The Neo4j label of the node to which this record is related.
    *   `"target_id"`: The unique identifier of the target node.

### Example (Generic)

```json
{
  "id": "unique-entity-123",
  "domain": "NEW_DOMAIN",
  "property_one": "value1",
  "property_two": 123,
  "connections": [
    {
      "type": "RELATED_TO",
      "target_label": "OTHER_DOMAIN",
      "target_id": "other-entity-456"
    }
  ]
}
```

## 2. Create Sample JSON Data File

Place your sample JSON data files in the `schemas/` directory. These files will be used by the `DomainManager` to infer the schema for your new domain when the API starts or when schemas are refreshed.

**Example**: `schemas/new_domain_data.json`

```json
[
  {
    "id": "item-A",
    "domain": "INVENTORY",
    "name": "Widget A",
    "quantity": 100,
    "connections": [
      {
        "type": "MANUFACTURED_BY",
        "target_label": "COMPANY",
        "target_id": "company-X"
      }
    ]
  }
]
```

## 3. (Optional) Create a Mapping File for Normalization

If your raw JSON data needs transformation before being imported into Neo4j, you can create a mapping file. This file allows you to:

*   **Rename Fields**: Change the name of a JSON key to a different property name in Neo4j.
*   **Type Conversions**: Convert string values to other data types (e.g., `int`, `float`, `bool`, `date`).
*   **Default Values**: Provide default values for fields that might be missing in your JSON data.

Place your mapping files in the `schemas/` directory.

### Mapping File Structure

```json
{
  "rename_fields": {
    "old_json_key": "new_neo4j_property_name"
  },
  "type_conversions": {
    "neo4j_property_name": "target_type"  // target_type can be "int", "float", "bool", "date"
  },
  "default_values": {
    "neo4j_property_name": "default_value"
  }
}
```

### Example: `schemas/inventory_mapping.json`

```json
{
  "rename_fields": {
    "product_name": "name",
    "qty": "quantity"
  },
  "type_conversions": {
    "quantity": "int"
  },
  "default_values": {
    "status": "available"
  }
}
```

## 4. Import Your Data

Use the `importer.py` script with your JSON data file and specify the domain. If you have a mapping file, include it using the `--mapping-file` flag.

```bash
python src/importer.py schemas/new_domain_data.json --domain INVENTORY --mapping-file schemas/inventory_mapping.json --merge
```

## 5. Verify in API

After importing, you can verify that your new domain and its schema are recognized by the API by calling the `/v1/info` endpoint:

```bash
curl http://localhost:8000/v1/info
```

You should see `INVENTORY` listed under `supported_domains` with its inferred properties and relationships.

You can then query your new domain:

```bash
curl "http://localhost:8000/v1/query/inventory?properties=name=Widget%20A"
```
