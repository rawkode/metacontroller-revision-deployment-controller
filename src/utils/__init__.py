from consumer_deployment_spec import ConsumerDeploymentSpec, hash_schema
from kubernetes.client import ApiClient
from kubernetes.client.models.v1_container import V1Container
from kubernetes.client.models.v1_label_selector import V1LabelSelector
from kubernetes.client.models.v1_pod_spec import V1PodSpec
from kubernetes.client.models.v1_pod_template_spec import V1PodTemplateSpec
from kubernetes.client.models.v1_replica_set import V1ReplicaSet
from kubernetes.client.models.v1_replica_set_spec import V1ReplicaSetSpec

import datetime
import sys


def request_in_to_objects(payload: dict):
    objects = []

    if 'children' not in payload:
        return []

    children = payload['children']

    for type, items in children.items():
        for name, item in items.items():
            if 'consumer.mindetic.gt8/schemaB64' not in item['metadata']['annotations']:
                print('Skipping ' + name + ' as no schemaB64')
                continue

            annotations = {k: v for k, v in filter(
                lambda t: t[0].startswith('consumer'), item['metadata']['annotations'].items())}

            object = {
                'type': type,
                'name': name,
                'replicas': item['spec']['replicas'],
                'image': item['spec']['template']['spec']['containers'][0]['image'],
                'annotations': annotations
            }
            objects.append(object)

    return objects


def objects_to_request_out(consumer_deployment_spec: ConsumerDeploymentSpec, objects: list):
    children = []

    for object in objects:
        if 'ReplicaSet.extensions/v1beta1' == object['type']:
            if 'name' in object:
                children.append(object_to_replica_set(
                    consumer_deployment_spec, object))
            else:
                children.append(new_replica_set(consumer_deployment_spec))

    api = ApiClient()
    response = api.sanitize_for_serialization(children)

    return {'children': response}


def new_replica_set(consumer_deployment_spec: ConsumerDeploymentSpec):
    print(consumer_deployment_spec)
    sys.stdout.flush()

    return V1ReplicaSet(
        api_version='extensions/v1beta1',
        kind='ReplicaSet',
        metadata={
            'generateName': consumer_deployment_spec.service + '-',
            'annotations': {
                'consumer.mindetic.gt8/schemaB64': consumer_deployment_spec.schema_b64,
                'consumer.mindetic.gt8/active': str(datetime.datetime.now())
            }
        },
        spec=V1ReplicaSetSpec(
            replicas=1,
            selector=V1LabelSelector(
                match_labels={
                    'service': consumer_deployment_spec.service,
                    'component': 'consumer'
                }),
            template=V1PodTemplateSpec(
                metadata={
                    'labels': {
                        'service': consumer_deployment_spec.service,
                        'component': 'consumer'
                    }
                },
                spec=V1PodSpec(
                    containers=[
                        V1Container(name='consumer',
                                    image=consumer_deployment_spec.image)
                    ],
                    init_containers=[
                        V1Container(name='schema-creator',
                                    image='gcr.io/gt8-mindetic/consumer-operator:2.0',
                                    args=['create_schema.py'],
                                    env=[
                                        {'name': 'SCHEMA_B64',
                                            'value': consumer_deployment_spec.schema_b64},
                                        {'name': 'SCHEMA_HASH',
                                            'value': consumer_deployment_spec.schema_hash},
                                        {'name': 'ELASTICSEARCH_URI',
                                            'value': consumer_deployment_spec.elasticsearch_uri}
                                    ])
                    ],
                )
            )
        )
    )


def object_to_replica_set(consumer_deployment_spec: ConsumerDeploymentSpec, object: dict):
    annotations = {k: v for k, v in filter(
        lambda t: t[0].startswith('consumer'), object['annotations'].items())}

    print('Applying annotations')
    print(annotations)
    sys.stdout.flush()

    schema_hash = hash_schema(
        object['annotations']['consumer.mindetic.gt8/schemaB64'])

    return V1ReplicaSet(
        api_version='extensions/v1beta1',
        kind='ReplicaSet',
        metadata={
            'name': object['name'],
            'annotations': annotations
        },
        spec=V1ReplicaSetSpec(
            replicas=1,
            selector=V1LabelSelector(
                match_labels={
                    'service': consumer_deployment_spec.service,
                    'component': 'consumer'
                }),
            template=V1PodTemplateSpec(
                metadata={
                    'labels': {
                        'service': consumer_deployment_spec.service,
                        'component': 'consumer'
                    }
                },
                spec=V1PodSpec(
                    containers=[
                        V1Container(name='consumer', image=object['image'])
                    ],
                    init_containers=[
                        V1Container(name='schema-creator',
                                    image='gcr.io/gt8-mindetic/consumer-operator:2.0',
                                    args=['create_schema.py'],
                                    env=[
                                        {'name': 'SCHEMA_B64',
                                            'value': object['annotations']['consumer.mindetic.gt8/schemaB64']},
                                        {'name': 'SCHEMA_HASH',
                                            'value': schema_hash},
                                        {'name': 'ELASTICSEARCH_URI',
                                            'value': consumer_deployment_spec.elasticsearch_uri},
                                    ])
                    ],
                )
            )
        )
    )
