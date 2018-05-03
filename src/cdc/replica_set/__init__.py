from cdc.utils.hash import hash_schema
from datetime import datetime
from dateutil.parser import parse as parse_date
from typing import Optional

import dateutil.parser


def load_date(date: Optional[str]) -> Optional[datetime]:
    if date is None:
        return None

    return parse_date(date)


class ReplicaSet:
    def __init__(self, name: Optional[str], created: Optional[str], init_containers: list, containers: list, replicas: int, annotations: dict):
        self.type = 'ReplicaSet.extensions/v1beta1'

        self.name = name
        self.created = load_date(created)

        self.replicas = replicas

        self.init_containers = init_containers
        self.containers = containers

        # Load only our own annotations
        self.annotations = {k: v for k, v in filter(
            lambda t: t[0].startswith('consumer.mindetic.gt8'), annotations.items())}

        self.schema_b64 = annotations['consumer.mindetic.gt8/schemaB64']
        self.schema_hash = hash_schema(self.schema_b64)

        self.active = False

        if 'consumer.mindetic.gt8/active' in annotations:
            self.active = True

    def set_active(self):
        self.annotations['consumer.mindetic.gt8/active'] = str(datetime.now())
        self.active = True

    def set_unactive(self):
        self.annotations.pop('consumer.mindetic.gt8/active', None)
        self.active = False
