from cdc import CDCSpec
from cdc.metacontroller import save_replica_set
from cdc.replica_set import ReplicaSet
from datetime import datetime


def get_spec():
    return CDCSpec(
        service='user-service',
        image='',
        schema_b64='',
        schema_alias='',
        elasticsearch_uri='',
        support_schemas=1
    )


def get_replica_set():
    created = datetime(2018, 10, 20, 9, 6, 3)

    return ReplicaSet(
        name='Name',
        created=created.isoformat(),
        init_containers=[{
            'name': 'schema-creator',
            'image': 'init:latest',
            'command': ['1', '2'],
            'args': ['2', '1'],
            'env': [
                {'name': 'name', 'value': 'value'}
            ]
        }],
        containers=[{
            'name': 'consumer',
            'image': 'normal:latest',
            'command': ['3', '4'],
            'args': ['5', '6'],
            'env': [
                {'name': 'env', 'value': 'cool'}
            ]
        }],
        annotations={
            'should not be collected': None,
            'consumer.mindetic.gt8/active': 'whatever',
            'consumer.mindetic.gt8/schemaB64': 'aGVsbG8K'
        },
        replicas=1
    )


def get_new_replica_set():
    return ReplicaSet(
        name=None,
        created=None,
        init_containers=[{
            'name': 'schema-creator',
            'image': 'init:latest',
            'command': ['1', '2'],
            'args': ['2', '1'],
            'env': [
                {'name': 'name', 'value': 'value'}
            ]
        }],
        containers=[{
            'name': 'consumer',
            'image': 'normal:latest',
            'command': ['3', '4'],
            'args': ['5', '6'],
            'env': [
                {'name': 'env', 'value': 'cool'}
            ]
        }],
        annotations={
            'should not be collected': None,
            'consumer.mindetic.gt8/active': 'whatever',
            'consumer.mindetic.gt8/schemaB64': 'aGVsbG8K'
        },
        replicas=1
    )
