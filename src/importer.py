import argparse
import json
import os
import logging
from dotenv import load_dotenv
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable, AuthError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

class Neo4jImporter:
    def __init__(self, uri, user, password):
        self.driver = None
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            self.driver.verify_connectivity()
            logging.info("Successfully connected to Neo4j.")
        except AuthError:
            logging.error("Neo4j authentication failed. Please check your credentials.")
            raise
        except ServiceUnavailable:
            logging.error(f"Could not connect to Neo4j at {uri}. Is the database running?")
            raise
        except Exception as e:
            logging.error(f"An unexpected error occurred during Neo4j connection: {e}")
            raise

        self.successful_imports = 0
        self.failed_imports = 0
        self.mappings = {}

    def close(self):
        if self.driver:
            self.driver.close()
            logging.info("Neo4j connection closed.")

    def import_data(self, file_path, domain_type, merge_on_conflict=False, batch_size=1000):
        logging.info(f"Starting import for file: {file_path} with domain: {domain_type}")
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logging.error(f"Malformed JSON in {file_path}: {e}")
            self.failed_imports += 1
            return
        except FileNotFoundError:
            logging.error(f"File not found: {file_path}")
            self.failed_imports += 1
            return

        records_to_process = []
        if isinstance(data, list):
            records_to_process = data
        else:
            records_to_process = [data]

        total_records = len(records_to_process)
        logging.info(f"Found {total_records} records to process.")

        for i in range(0, total_records, batch_size):
            batch = records_to_process[i:i + batch_size]
            self._process_batch(batch, domain_type, merge_on_conflict)

    def _apply_mappings(self, record):
        transformed_record = record.copy()

        # Apply renames
        for old_name, new_name in self.mappings.get("rename_fields", {}).items():
            if old_name in transformed_record:
                transformed_record[new_name] = transformed_record.pop(old_name)

        # Apply type conversions and default values
        for field, conversion_type in self.mappings.get("type_conversions", {}).items():
            if field in transformed_record:
                try:
                    if conversion_type == "int":
                        transformed_record[field] = int(transformed_record[field])
                    elif conversion_type == "float":
                        transformed_record[field] = float(transformed_record[field])
                    elif conversion_type == "bool":
                        transformed_record[field] = str(transformed_record[field]).lower() in ['true', '1', 't', 'y']
                    elif conversion_type == "date":
                        # This is a basic date conversion, might need more robust parsing for various formats
                        from datetime import datetime
                        transformed_record[field] = datetime.fromisoformat(transformed_record[field].replace('Z', '+00:00'))
                except ValueError as e:
                    logging.warning(f"Could not convert field '{field}' to type '{conversion_type}': {e}")
            elif field in self.mappings.get("default_values", {}):
                transformed_record[field] = self.mappings["default_values"][field]

        return transformed_record

    def _process_batch(self, batch, domain_type, merge_on_conflict):
        with self.driver.session() as session:
            tx = None
            try:
                tx = session.begin_transaction()
                for record in batch:
                    if not isinstance(record, dict):
                        logging.warning(f"Skipping malformed record (not a dictionary): {record}")
                        self.failed_imports += 1
                        continue

                    # Apply mappings and normalization
                    processed_record = self._apply_mappings(record)

                    record_identifier = processed_record.get('id') or processed_record.get('name') or processed_record.get('uuid')
                    if not record_identifier:
                        logging.warning(f"Record missing common identifier (id, name, or uuid) after mapping: {processed_record}")

                    properties = {k: v for k, v in processed_record.items() if k not in ['domain', 'connections']}
                    label = domain_type

                    # Create/Merge Node
                    query_verb = "MERGE" if merge_on_conflict else "CREATE"
                    if merge_on_conflict and 'id' in properties:
                        node_query = f"{query_verb} (n:{label} {{id: $props.id}})
                                       ON CREATE SET n = $props
                                       ON MATCH SET n = $props"
                    else:
                        node_query = f"CREATE (n:{label} $props)"

                    tx.run(node_query, props=properties)
                    self.successful_imports += 1
                    logging.debug(f"Successfully processed node for domain {domain_type}: {record_identifier or 'no-id'}")

                    # Process Relationships
                    if 'connections' in processed_record and isinstance(processed_record['connections'], list):
                        for connection in processed_record['connections']:
                            rel_type = connection.get('type')
                            target_label = connection.get('target_label')
                            target_id = connection.get('target_id')

                            if all([rel_type, target_label, target_id]):
                                rel_query = f"MATCH (a:{label} {{id: $source_id}})
                                              MATCH (b:{target_label} {{id: $target_id}})
                                              MERGE (a)-[:{rel_type}]->(b)"
                                tx.run(rel_query, source_id=record_identifier, target_id=target_id)
                                self.successful_imports += 1 # Count relationship creation as a successful import operation
                                logging.debug(f"Successfully created relationship {rel_type} from {record_identifier} to {target_id}")
                            else:
                                logging.warning(f"Malformed connection in record {record_identifier}: {connection}")
                                self.failed_imports += 1
                tx.commit()
            except Exception as e:
                if tx:
                    tx.rollback()
                self.failed_imports += len(batch) # Mark all records in batch as failed
                logging.error(f"Transaction failed for batch. Rolling back. Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Import JSON data into Neo4j.")
    parser.add_argument("file", help="Path to the JSON data file.")
    parser.add_argument("--domain", required=True, help="Domain type for the data (e.g., WEATHER, HEALTH).")
    parser.add_argument("--uri", default=os.getenv("NEO4J_URI"),
                        help="Neo4j URI (default: NEO4J_URI from .env).")
    parser.add_argument("--user", default=os.getenv("NEO4J_USER"),
                        help="Neo4j User (default: NEO4J_USER from .env).")
    parser.add_argument("--password", default=os.getenv("NEO4J_PASSWORD"),
                        help="Neo4j Password (default: NEO4J_PASSWORD from .env).")
    parser.add_argument("--merge", action="store_true",
                        help="Use MERGE (upsert) logic instead of CREATE for conflicting records.")
    parser.add_argument("--batch-size", type=int, default=1000,
                        help="Number of records to process in each batch (default: 1000).")
    parser.add_argument("--mapping-file", help="Path to a JSON file defining custom mappings and schema normalization rules.")

    args = parser.parse_args()

    # Validate required parameters
    if not all([args.uri, args.user, args.password]):
        logging.error("Neo4j URI, user, and password must be provided via arguments or .env file.")
        exit(1)

    importer = None
    try:
        importer = Neo4jImporter(args.uri, args.user, args.password)

        if args.mapping_file:
            try:
                with open(args.mapping_file, 'r') as f:
                    importer.mappings = json.load(f)
                logging.info(f"Loaded mapping file: {args.mapping_file}")
            except (FileNotFoundError, json.JSONDecodeError) as e:
                logging.error(f"Error loading mapping file {args.mapping_file}: {e}")
                exit(1)

        importer.import_data(args.file, args.domain, args.merge, args.batch_size)
        logging.info("\n--- Import Summary ---")
        logging.info(f"Successful imports: {importer.successful_imports}")
        logging.info(f"Failed imports: {importer.failed_imports}")
        logging.info("----------------------")
    except (AuthError, ServiceUnavailable):
        exit(1)
    except Exception as e:
        logging.error(f"An unhandled error occurred during import: {e}")
        exit(1)
    finally:
        if importer:
            importer.close()

if __name__ == "__main__":
    main()
