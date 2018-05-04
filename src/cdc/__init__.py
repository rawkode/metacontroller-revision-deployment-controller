from cdc.utils.hash import hash_schema


class CDCSpec:
    def __init__(self, service: str, image: str, schema_b64: str, schema_alias: str, support_schemas: int):
        self.service = service
        self.image = image
        self.schema_b64 = schema_b64
        self.schema_hash = hash_schema(schema_b64)
        self.schema_alias = schema_alias
        self.support_schemas = support_schemas
