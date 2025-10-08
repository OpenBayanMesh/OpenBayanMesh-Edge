from fastapi import APIRouter, Depends, HTTPException, status, Query
from datetime import datetime
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from neo4j import GraphDatabase
import os

from src.dependencies import get_api_version
from src.main import fatal_error_count, TELEMETRY_ENABLED # Import the global error counter and TELEMETRY_ENABLED
from src.domain_manager import domain_manager # Import the domain manager

router = APIRouter(dependencies=[Depends(get_api_version)])

# Neo4j Driver setup
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

driver = None

def get_neo4j_driver():
    global driver
    if driver is None:
        try:
            driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
            driver.verify_connectivity()
            print("Neo4j driver created and verified.")
        except Exception as e:
            print(f"Failed to create Neo4j driver: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not connect to Neo4j")
    return driver

# Pydantic Models
class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str

class DomainSchema(BaseModel):
    properties: Dict[str, str]
    relationships: List[Dict[str, str]]
    deprecated: Optional[bool] = False
    sunset_date: Optional[str] = None

class InfoResponse(BaseModel):
    app_name: str
    api_version: str
    supported_domains: Dict[str, DomainSchema]

class Neo4jNode(BaseModel):
    id: int
    labels: List[str]
    properties: Dict[str, Any]

class Neo4jRelationship(BaseModel):
    id: int
    type: str
    start_node_id: int
    end_node_id: int
    properties: Dict[str, Any]

class MetricsResponse(BaseModel):
    message: str
    metrics: Dict[str, Any]
    fatal_errors: int

# Helper function for dynamic Cypher query construction
def build_cypher_query(domain: str, filters: Dict[str, Any]) -> (str, Dict[str, Any]):
    match_clause = f"MATCH (n:{domain})"
    where_clauses = []
    params = {}

    for key, value in filters.items():
        # Basic sanitization to prevent injection, though parameterized queries are the main defense
        if not re.match(r"^[a-zA-Z0-9_]+$", key): # Ensure key is alphanumeric
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid filter key: {key}")
        where_clauses.append(f"n.{key} = ${key}")
        params[key] = value

    query = match_clause
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    query += " RETURN n"
    return query, params

# API Endpoints
@router.get("/health", response_model=HealthResponse, tags=["v1 - System Status"])
async def health_v1():
    return {"status": "healthy", "timestamp": datetime.now(), "version": "v1"}

@router.get("/info", response_model=InfoResponse, tags=["v1 - System Status"])
async def info_v1():
    return {"app_name": "OpenBayanMesh-Edge", "api_version": "v1", "supported_domains": domain_manager.get_all_domains()}

    if domain.upper() not in domain_manager.get_all_domains():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Domain '{domain}' not supported. Available domains: {list(domain_manager.get_all_domains().keys())}")

    domain_info = domain_manager.get_domain_schema(domain)
    if domain_info and domain_info.get("deprecated"):
        detail_msg = f"Domain '{domain}' is deprecated."
        if domain_info.get("sunset_date"):
            detail_msg += f" It will be removed after {domain_info["sunset_date"]}."
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail_msg)

    filters = {}
    if properties:
        domain_schema = domain_manager.get_domain_schema(domain)
        if not domain_schema:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Schema for domain '{domain}' not found.")

        for prop_filter in properties.split(','):
            if '=' in prop_filter:
                key, value = prop_filter.split('=', 1)
                key = key.strip()
                value = value.strip()

                if key not in domain_schema["properties"]:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unsupported property '{key}' for domain '{domain}'. Available properties: {list(domain_schema["properties"].keys())}")

                # Basic type validation (can be expanded)
                expected_type = domain_schema["properties"][key]
                try:
                    if expected_type == "int":
                        value = int(value)
                    elif expected_type == "float":
                        value = float(value)
                    elif expected_type == "bool":
                        value = value.lower() in ['true', '1', 't', 'y']
                    # Add more type conversions as needed
                except ValueError:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid type for property '{key}'. Expected {expected_type}.")

                filters[key] = value
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid property filter format: {prop_filter}. Expected 'key=value'.")

    cypher_query, params = build_cypher_query(domain.upper(), filters)
    driver = get_neo4j_driver()
    nodes = []
    try:
        with driver.session(database=NEO4J_DATABASE) as session:
            result = session.run(cypher_query, params)
            for record in result:
                node = record["n"]
                nodes.append(Neo4jNode(
                    id=node.id,
                    labels=list(node.labels),
                    properties=dict(node.items())
                ))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Neo4j query failed: {e}")

    return nodes

@router.get("/query/{domain}/relationships", tags=["v1 - Data Operations"], response_model=List[Neo4jRelationship])
async def query_domain_relationships(
    domain: str,
    rel_type: Optional[str] = Query(None, description="Type of relationship to filter by"),
    target_label: Optional[str] = Query(None, description="Label of the target node in the relationship"),
    properties: Optional[str] = Query(None, description="Comma-separated list of relationship properties to filter by (e.g., 'since=2023')")
):
    if domain.upper() not in domain_manager.get_all_domains():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Domain '{domain}' not supported. Available domains: {list(domain_manager.get_all_domains().keys())}")

    domain_info = domain_manager.get_domain_schema(domain)
    if domain_info and domain_info.get("deprecated"):
        detail_msg = f"Domain '{domain}' is deprecated."
        if domain_info.get("sunset_date"):
            detail_msg += f" It will be removed after {domain_info["sunset_date"]}."
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail_msg)

    match_clause = f"MATCH (a:{domain.upper()})-[r]-(b)"
    where_clauses = []
    params = {}

    if rel_type:
        match_clause = f"MATCH (a:{domain.upper()})-[r:{rel_type}]-(b)"

    if target_label:
        where_clauses.append(f"b:{target_label}")

    if properties:
        # This part needs to be more sophisticated to handle relationship properties vs node properties
        # For simplicity, assuming relationship properties for now
        for prop_filter in properties.split(','):
            if '=' in prop_filter:
                key, value = prop_filter.split('=', 1)
                where_clauses.append(f"r.{key.strip()} = ${key.strip()}")
                params[key.strip()] = value.strip()
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid property filter format: {prop_filter}. Expected 'key=value'.")

    query = match_clause
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    query += " RETURN r"

    driver = get_neo4j_driver()
    relationships = []
    try:
        with driver.session(database=NEO4J_DATABASE) as session:
            result = session.run(query, params)
            for record in result:
                rel = record["r"]
                relationships.append(Neo4jRelationship(
                    id=rel.id,
                    type=rel.type,
                    start_node_id=rel.start_node.id,
                    end_node_id=rel.end_node.id,
                    properties=dict(rel.items())
                ))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Neo4j query failed: {e}")

    return relationships

@router.post("/admin/refresh-schemas", tags=["Admin"]) # This endpoint should be protected in a real application
async def refresh_schemas():
    domain_manager.refresh_schemas()
    return {"message": "Domain schemas refreshed successfully."}

@router.post("/admin/deprecate-domain/{domain_name}", tags=["Admin"]) # This endpoint should be protected
async def deprecate_domain_endpoint(domain_name: str, sunset_date: Optional[str] = None):
    domain_manager.deprecate_domain(domain_name, sunset_date)
    return {"message": f"Domain '{domain_name}' marked as deprecated."}

@router.get("/metrics", response_model=MetricsResponse, tags=["v1 - System Status"])
async def metrics_v1():
    if not TELEMETRY_ENABLED:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Telemetry is disabled. Enable TELEMETRY_ENABLED in environment variables to access metrics.")
    # Placeholder for metrics collection
    return {"message": "Metrics endpoint for v1", "metrics": {}, "fatal_errors": fatal_error_count}

@router.get("/node/{node_id}", response_model=Neo4jNode, tags=["v1 - Data Operations"])
async def get_node_by_id(node_id: int):
    driver = get_neo4j_driver()
    query = "MATCH (n) WHERE id(n) = $node_id RETURN n"
    with driver.session(database=NEO4J_DATABASE) as session:
        result = session.run(query, node_id=node_id)
        record = result.single()
        if record:
            node = record["n"]
            return Neo4jNode(
                id=node.id,
                labels=list(node.labels),
                properties=dict(node.items())
            )
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Node not found")
