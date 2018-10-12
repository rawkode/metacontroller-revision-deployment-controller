from cdc.utils.hash import hash_schema


class CDCSpec:
    def __init__(self, service: str, image: str, schema_b64: str, schema_alias: str, support_schemas: int, consumer_tooling_version: str, env_config_map: str = None, mount_secrets: list = []):
        self.service = service
        self.image = image
        self.schema_b64 = schema_b64
        self.schema_hash = hash_schema(schema_b64)
        self.schema_alias = schema_alias
        self.support_schemas = support_schemas
        self.env_config_map = env_config_map
        self.mount_secrets = mount_secrets
        self.consumer_tooling_version = consumer_tooling_version
