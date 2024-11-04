from typing import Dict, List

class ConfigValidator:
    def __init__(self):
        self.schemas = {}
        self.validators = {}

    def register_schema(self, section: str, schema: Dict):
        self.schemas[section] = schema

    def validate_config(self, config: Dict) -> List[str]:
        errors = []
        for section, schema in self.schemas.items():
            if section in config:
                section_errors = self._validate_section(config[section], schema)
                errors.extend(section_errors)
        return errors 