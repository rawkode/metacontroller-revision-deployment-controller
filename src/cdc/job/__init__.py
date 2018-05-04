from cdc.utils.hash import hash_schema


class Job:
    def __init__(self, name: str, containers: list, annotations: dict):
        self.type = ''
        self.name = name
        self.containers = containers
        self.annotations = annotations

        if 'consumer.mindetic.gt8/schemaB64' not in annotations:
            raise Exception('Could not determine schemaB64 for Job')

        self.schema_b64 = annotations['consumer.mindetic.gt8/schemaB64']
        self.schema_hash = hash_schema(self.schema_b64)
