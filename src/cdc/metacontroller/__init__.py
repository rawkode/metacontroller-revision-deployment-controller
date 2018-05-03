from cdc import CDCSpec
from cdc.job import Job
from cdc.replica_set import ReplicaSet
from sys import stdout

import kubernetes.client as k8s_client
import kubernetes.client.models as k8s


def load_parent(payload: dict):
    spec = payload['spec']

    return CDCSpec(
        service=spec['service'],
        image=spec['image'],
        schema_b64=spec['schemaB64'],
        schema_alias=spec['schemaAlias'],
        elasticsearch_uri=spec['elasticsearchUri'],
        support_schemas=int(spec['supportSchemas'])
    )


def load_children(payload: dict) -> dict:
    replica_sets = []
    jobs = []

    for typ, objs in payload.items():
        for _, obj in objs.items():
            if typ == 'ReplicaSet.extensions/v1beta1':
                replica_sets.append(load_replica_set(obj))
            elif typ == 'Job.batch/v1':
                jobs.append(load_job(obj))
            else:
                print('Failed to load type "' + typ + '". Moving on.')
                stdout.flush()

    return {'jobs': jobs, 'replica_sets': replica_sets}


def save_children(spec: CDCSpec, children: dict) -> dict:
    response = {'children': []}

    for _, objs in children.items():
        for obj in objs:
            if type(obj) == ReplicaSet:
                response['children'].append(save_replica_set(spec, obj))
            elif type(obj) == Job:
                response['children'].append(save_job(spec, obj))

    api = k8s_client.ApiClient()
    return api.sanitize_for_serialization(response)


def load_job(payload: dict):
    return None


def save_job(spec: CDCSpec, job: Job):
    return None


def load_replica_set(payload: dict):
    if 'metadata' not in payload or 'name' not in payload['metadata']:
        return None

    name = payload['metadata']['name']

    if 'metadata' not in payload or 'annotations' not in payload['metadata']:
        print('Losing replicaSet (' + name + '), could not find schema_b64')

    # Load Our Annotations
    annotations = {k: v for k, v in filter(
        lambda t: t[0].startswith('consumer.mindetic.gt8'), payload['metadata']['annotations'].items())}

    init_containers = []
    if 'initContainers' in payload['spec']['template']['spec']:
        init_containers = payload['spec']['template']['spec']['initContainers']

    return ReplicaSet(
        name=name,
        created=payload['metadata']['creationTimestamp'],
        init_containers=init_containers,
        containers=payload['spec']['template']['spec']['containers'],
        annotations=annotations,
        replicas=int(payload['spec']['replicas'])
    )


def save_replica_set(spec: CDCSpec, replica_set: ReplicaSet):
    metadata = {
        'annotations': replica_set.annotations
    }

    if replica_set.name is None:
        metadata['generateName'] = spec.service + '-'
    else:
        metadata['name'] = replica_set.name

    containers = []

    for container in replica_set.containers:
        containers.append(k8s.V1Container(
            name=container['name'],
            image=container['image'],
            command=container.get('command', None),
            args=container.get('args', []),
            env=container['env'],
            image_pull_policy=container['imagePullPolicy']
        ))

    init_containers = []

    for container in replica_set.init_containers:
        init_containers.append(k8s.V1Container(
            name=container['name'],
            image=container['image'],
            command=container.get('command', None),
            args=container.get('args', []),
            env=container['env'],
            image_pull_policy=container['imagePullPolicy']
        ))

    return k8s.V1ReplicaSet(
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
                    containers=containers,
                    init_containers=init_containers
                )
            )
        )
    )
