from cdc.replica_set import ReplicaSet
from datetime import datetime
from watch import remove_oldest


def test_remove_oldest():
    created1 = datetime(2018, 10, 20, 9, 6, 3)

    replica_set1 = ReplicaSet(
        name='Name',
        created=created1.isoformat(),
        init_containers=[],
        containers=[],
        annotations={
            'should not be collected': None,
            'consumer.mindetic.gt8/schemaB64': 'aGVsbG8K'
        },
        replicas=1
    )

    created2 = datetime(2018, 10, 20, 9, 6, 2)

    replica_set2 = ReplicaSet(
        name='Name',
        created=created2.isoformat(),
        init_containers=[],
        containers=[],
        annotations={
            'should not be collected': None,
            'consumer.mindetic.gt8/schemaB64': 'aGVsbG8K'
        },
        replicas=1
    )

    created3 = datetime(2018, 10, 20, 9, 6, 0)

    replica_set3 = ReplicaSet(
        name='Name',
        created=created3.isoformat(),
        init_containers=[],
        containers=[],
        annotations={
            'should not be collected': None,
            'consumer.mindetic.gt8/schemaB64': 'aGVsbG8K'
        },
        replicas=1
    )

    children = remove_oldest([replica_set1, replica_set2, replica_set3])
    assert children == [replica_set1, replica_set2]

    # children = remove_oldest([replica_set1, replica_set3, replica_set2])
    # assert children == [replica_set1, replica_set2]

    # children = remove_oldest([replica_set3, replica_set2, replica_set1])
    # assert children == [replica_set2, replica_set1]
