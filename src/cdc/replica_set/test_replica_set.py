from cdc.replica_set import ReplicaSet
from datetime import datetime


def test_active_replica_set():
    created = datetime(2018, 10, 20, 9, 6, 3)

    replica_set = ReplicaSet(
        name='Name',
        created=created.isoformat(),
        init_containers=[],
        containers=[],
        annotations={
            'should not be collected': None,
            'consumer.mindetic.gt8/active': 'whatever',
            'consumer.mindetic.gt8/schemaB64': 'aGVsbG8K'
        },
        replicas=1
    )

    assert replica_set.type == 'ReplicaSet.extensions/v1beta1'
    assert replica_set.name == 'Name'
    assert replica_set.schema_b64 == 'aGVsbG8K'
    assert replica_set.schema_hash == '30463dcbfb1813ccc89b669a71122815f8428e79bf47fe6a4f35253623a7f6ad'
    assert replica_set.created == created
    assert replica_set.active == True
    assert replica_set.replicas == 1
    assert 'should not be collected' not in replica_set.annotations


def test_unactive_replica_set():
    created = datetime(2014, 5, 28, 22, 5, 1)

    replica_set = ReplicaSet(
        name='Another Name',
        created=created.isoformat(),
        init_containers=[],
        containers=[],
        annotations={
            'consumer.mindetic.gt8/schemaB64': 'R28gQXdheQo=',
            'should not be collected': None,
            'whatever': None,
            'consumer.mindetic.gt8/random': True,
        },
        replicas=2
    )

    assert replica_set.type == 'ReplicaSet.extensions/v1beta1'
    assert replica_set.name == 'Another Name'
    assert replica_set.schema_b64 == 'R28gQXdheQo='
    assert replica_set.schema_hash == '3ad8708f9d0c21d094b7062e9e72a25e146f3730770c8f09f3097653e092df05'
    assert replica_set.created == created
    assert replica_set.active == False
    assert replica_set.replicas == 2
    assert 'should not be collected' not in replica_set.annotations
    assert 'whatever' not in replica_set.annotations
    assert 'consumer.mindetic.gt8/random' in replica_set.annotations
    assert True == replica_set.annotations['consumer.mindetic.gt8/random']


def test_new_replica_set():
    replica_set = ReplicaSet(
        name=None,
        created=None,
        init_containers=[],
        containers=[],
        annotations={
            'consumer.mindetic.gt8/schemaB64': 'SCHEMA'
        },
        replicas=1
    )

    assert replica_set.type == 'ReplicaSet.extensions/v1beta1'
    assert replica_set.name == None
    assert replica_set.created == None


def test_set_active():
    created = datetime(2018, 10, 20, 9, 6, 3)

    replica_set = ReplicaSet(
        name='Name',
        created=created.isoformat(),
        init_containers=[],
        containers=[],
        annotations={
            'should not be collected': None,
            'consumer.mindetic.gt8/schemaB64': 'aGVsbG8K'
        },
        replicas=1
    )

    assert replica_set.active == False
    assert 'consumer.mindetic.gt8/active' not in replica_set.annotations

    replica_set.set_active()

    assert replica_set.active == True
    assert 'consumer.mindetic.gt8/active' in replica_set.annotations


def test_set_unactive():
    created = datetime(2018, 10, 20, 9, 6, 3)

    replica_set = ReplicaSet(
        name='Name',
        created=created.isoformat(),
        init_containers=[],
        containers=[],
        annotations={
            'should not be collected': None,
            'consumer.mindetic.gt8/active': 'whatever',
            'consumer.mindetic.gt8/schemaB64': 'aGVsbG8K'
        },
        replicas=1
    )

    assert replica_set.active == True
    assert 'consumer.mindetic.gt8/active' in replica_set.annotations

    replica_set.set_unactive()

    assert replica_set.active == False
    assert 'consumer.mindetic.gt8/active' not in replica_set.annotations
