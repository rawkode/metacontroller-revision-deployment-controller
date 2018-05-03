from cdc.utils.hash import hash_schema


class Job:
    def __init__(self, name: str, schema_b64: str, containers: list, annotations: dict):
        self.type = ''
        self.name = name
        self.schema_b64 = schema_b64
        self.schema_hash = hash_schema(schema_b64)
        self.containers = containers
        self.annotations = annotations
