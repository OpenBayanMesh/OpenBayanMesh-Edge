#!/bin/bash

# Wait for Neo4j to be ready
until curl -s http://localhost:7474/ > /dev/null; do
  echo "Waiting for Neo4j to start..."
  sleep 5
done

echo "Neo4j started. Running initialization scripts..."

# Example: Create a unique constraint
# cypher-shell -u neo4j -p $NEO4J_PASSWORD "CREATE CONSTRAINT ON (n:Node) ASSERT n.id IS UNIQUE;"

# Example: Create some initial data
# cypher-shell -u neo4j -p $NEO4J_PASSWORD "CREATE (n:Greeting {message: 'Hello, Neo4j!'});"

echo "Neo4j initialization complete."
