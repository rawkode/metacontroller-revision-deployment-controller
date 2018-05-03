from hashlib import sha256


def hash_schema(schema: str):
    return sha256(schema.encode('utf-8')).hexdigest()


class ConsumerDeploymentSpec:
    def __init__(self, service: str, image: str, schema_b64: str, schema_alias: str, elasticsearch_uri: str, support_schemas: int):
        self.service = service
        self.image = image
        self.schema_b64 = schema_b64
        self.schema_hash = hash_schema(schema_b64)
        self.schema_alias = schema_alias
        self.elasticsearch_uri = elasticsearch_uri
        self.support_schemas = support_schemas
