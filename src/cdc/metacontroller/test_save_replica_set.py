from cdc import CDCSpec
from cdc.metacontroller import save_replica_set
from cdc.metacontroller.test_utils import get_new_replica_set, get_replica_set, get_spec
from cdc.replica_set import ReplicaSet
from datetime import datetime

import kubernetes.client.models as k8s


def test_save_replica_set():
    spec = get_spec()
    replica_set = get_replica_set()

    metadata = {
        'annotations': replica_set.annotations
    }
    metadata['name'] = replica_set.name

    assert save_replica_set(spec, replica_set) == k8s.V1ReplicaSet(
        api_version='extensions/v1beta1',
        kind='ReplicaSet',
        metadata=metadata,
        spec=k8s.V1ReplicaSetSpec(
            replicas=1,
            selector=k8s.V1LabelSelector(
                match_labels={
                    'service': spec.service,
                    'component': 'consumer'
                }),
            template=k8s.V1PodTemplateSpec(
                metadata={
                    'labels': {
                        'service': spec.service,
                        'component': 'consumer'
                    }
                },
                spec=k8s.V1PodSpec(
                    containers=[
                        k8s.V1Container(
                            name='consumer',
                            image='normal:latest',
                            command=['3', '4'],
                            args=['5', '6'],
                            env=[
                                {'name': 'env', 'value': 'cool'}
                            ],
                            image_pull_policy='IfNotPresent'
                        )
                    ],
                    init_containers=[
                        k8s.V1Container(
                            name='schema-creator',
                            image='init:latest',
                            command=['1', '2'],
                            args=['2', '1'],
                            env=[
                                {'name': 'name', 'value': 'value'}
                            ],
                            image_pull_policy='IfNotPresent'
                        )
                    ]
                )
            )
        )
    )


def test_save_new_replica_set():
    spec = get_spec()

    replica_set = get_new_replica_set()

    metadata = {
        'annotations': replica_set.annotations
    }
    metadata['generateName'] = spec.service + '-'

    assert save_replica_set(spec, replica_set) == k8s.V1ReplicaSet(
        api_version='extensions/v1beta1',
        kind='ReplicaSet',
        metadata=metadata,
        spec=k8s.V1ReplicaSetSpec(
            replicas=1,
            selector=k8s.V1LabelSelector(
                match_labels={
                    'service': spec.service,
                    'component': 'consumer'
                }),
            template=k8s.V1PodTemplateSpec(
                metadata={
                    'labels': {
                        'service': spec.service,
                        'component': 'consumer'
                    }
                },
                spec=k8s.V1PodSpec(
                    containers=[
                        k8s.V1Container(
                            name='consumer',
                            image='normal:latest',
                            command=['3', '4'],
                            args=['5', '6'],
                            env=[
                                {'name': 'env', 'value': 'cool'}
                            ],
                            image_pull_policy='IfNotPresent'
                        )
                    ],
                    init_containers=[
                        k8s.V1Container(
                            name='schema-creator',
                            image='init:latest',
                            command=['1', '2'],
                            args=['2', '1'],
                            env=[
                                {'name': 'name', 'value': 'value'}
                            ],
                            image_pull_policy='IfNotPresent'
                        )
                    ]
                )
            )
        )
    )
