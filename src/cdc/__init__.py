from cdc.utils.hash import hash_schema


class CDCSpec:
    def __init__(self, service: str, image: str, schema_b64: str, schema_alias: str, elasticsearch_uri: str, kafka_host: str, kafka_topic: str, support_schemas: int):
        self.service = service
        self.image = image
        self.schema_b64 = schema_b64
        self.schema_hash = hash_schema(schema_b64)
        self.schema_alias = schema_alias
        self.elasticsearch_uri = elasticsearch_uri
        self.kafka_host = kafka_host
        self.kafka_topic = kafka_topic
        self.support_schemas = support_schemas
