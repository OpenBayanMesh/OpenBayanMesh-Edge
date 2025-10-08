import json
import os
import logging

logger = logging.getLogger(__name__)

class DomainManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DomainManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.domains = {}
        self._initialized = True
        self._load_initial_schemas()

    def _load_initial_schemas(self):
        # Placeholder for loading schemas from a predefined location or configuration
        # For now, we can add some mock data or load from a 'schemas' directory
        # This will be enhanced later to integrate with the importer.
        logger.info("Loading initial domain schemas...")
        schemas_dir = os.path.join(os.path.dirname(__file__), '..', 'schemas')
        if os.path.exists(schemas_dir):
            for filename in os.listdir(schemas_dir):
                if filename.endswith("_data.json"):
                    domain_name = filename.replace("_data.json", "").upper()
                    file_path = os.path.join(schemas_dir, filename)
                    try:
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                            if isinstance(data, list) and data:
                                # Infer schema from the first object in the list
                                self.add_domain_schema(domain_name, data[0])
                            elif isinstance(data, dict):
                                self.add_domain_schema(domain_name, data)
                            logger.info(f"Inferred initial schema for domain: {domain_name}")
                    except Exception as e:
                        logger.error(f"Error loading initial schema from {file_path}: {e}")
        else:
            logger.warning(f"Schemas directory not found at {schemas_dir}. No initial schemas loaded.")

    def add_domain_schema(self, domain_name: str, sample_data: dict):
        # Infer schema from sample_data
        schema = {"properties": {}, "relationships": []}
        for key, value in sample_data.items():
            if key == "connections" and isinstance(value, list):
                for conn in value:
                    if "type" in conn and "target_label" in conn:
                        schema["relationships"].append({"type": conn["type"], "target_label": conn["target_label"]})
            elif key != "domain": # 'domain' is used for label, not a property
                schema["properties"][key] = str(type(value).__name__)
        self.domains[domain_name.upper()] = schema
        logger.info(f"Domain schema added/updated for: {domain_name.upper()}")

    def deprecate_domain(self, domain_name: str, sunset_date: str = None):
        domain = self.domains.get(domain_name.upper())
        if domain:
            domain["deprecated"] = True
            domain["sunset_date"] = sunset_date
            logger.warning(f"Domain '{domain_name.upper()}' marked as deprecated. Sunset date: {sunset_date or 'N/A'}")
        else:
            logger.warning(f"Attempted to deprecate non-existent domain: {domain_name.upper()}")

    def get_all_domains(self) -> dict:
        return self.domains

    def get_domain_schema(self, domain_name: str) -> dict:
        return self.domains.get(domain_name.upper())

    def refresh_schemas(self):
        """Refreshes all schemas, e.g., after an import operation."""
        self.domains = {}
        self._load_initial_schemas()
        logger.info("Domain schemas refreshed.")

domain_manager = DomainManager()
