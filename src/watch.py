from cdc import CDCSpec
from cdc.metacontroller import load_children, load_parent, save_children
from cdc.replica_set import ReplicaSet
from cdc.job import Job
from flask import Flask, request, jsonify
from json import dumps
from pprint import pprint
from sys import stdout
from typing import Iterable, Optional
import random
import string

app = Flask(__name__)


@app.route('/watch', methods=['POST'])
def watch():
    print("New Request", flush=True)

    payload = request.get_json()

    print('Payload Received:', flush=True)
    print(payload, flush=True)

    parent = load_parent(payload['parent'])
    children = load_children(payload['children'])

    print('Parent Received:', flush=True)
    print(parent, flush=True)

    print('Children Received:', flush=True)
    print(children, flush=True)

    response = process(
        spec=parent,
        replica_sets=children['replica_sets'],
        jobs=children['jobs']
    )

    print('Sending Response:', flush=True)
    print(response, flush=True)

    return jsonify(response), 200


def process(spec: CDCSpec, replica_sets: Iterable[ReplicaSet], jobs: Iterable[Job]):
    active_replica_set = schema_has_replica_set(spec, replica_sets)

    children = []

    if active_replica_set is None:
        children = launch_new_replica_set(spec, replica_sets, jobs)

    if active_replica_set is True:
        children = update_active_replica_set(spec, replica_sets, jobs)
    else:
        children = promote_unactive_replica_set(spec, replica_sets, jobs)

    # Do we have too many ReplicaSets?
    if len(children['replica_sets']) > spec.support_schemas:
        children['replica_sets'] = remove_oldest(children['replica_sets'])

    # Convert to Kubernetes Objects
    response = save_children(spec, children)

    return response


def schema_has_replica_set(spec: CDCSpec, replica_sets: Iterable[ReplicaSet]) -> Optional[bool]:
    """
    Checks if the proposed schema already has a ReplicaSet consuming events.

    Returns True is it is the active ReplicaSet
    Returns False if it is an unactive ReplicaSet
    Returns None if no ReplicaSet is consuming for this schema
    """
    for replica_set in replica_sets:
        if replica_set.schema_b64 == spec.schema_b64:
            if replica_set.active:
                return True

            return False

    return None


def schema_is_active_replica_set(spec: CDCSpec, replica_sets: Iterable[ReplicaSet]) -> bool:
    for replica_set in replica_sets:
        if spec.schema_b64 == replica_set.schema_b64 and replica_set.active == True:
            return True

    return False


def remove_oldest(replica_sets: Iterable[ReplicaSet]) -> Iterable[ReplicaSet]:
    oldest_value = None

    for replica_set in replica_sets:
        if replica_set.active is False:
            if oldest_value is None:
                oldest_value = replica_set
            elif oldest_value.created > replica_set.created:
                oldest_value = replica_set

    replica_sets.remove(oldest_value)

    return replica_sets

# When we launch a new ReplicaSet, we can ignore any current jobs. These will
# be removed by the metacontroller because we don't return them. This will stop
# any current jobs from finishing and changing our alias. We only want the one
# we're about to return.


def launch_new_replica_set(spec: CDCSpec, replica_sets: Iterable[ReplicaSet], jobs: Iterable[Job]) -> dict:
    print("\n\n\nLAUNCHING NEW\n\n\n", flush=True)

    new_replica_set = ReplicaSet(
        name=None,
        created=None,
        annotations={
            'consumer.mindetic.gt8/schemaB64': spec.schema_b64
        },
        init_containers=[
            {
                'name': 'schema-creator',
                'image': 'gcr.io/gt8-mindetic/consumer-tooling/scripts:2.0',
                'imagePullPolicy': 'Always',
                'args': ['create_schema.py'],
                'env': [
                    {'name': 'SCHEMA_B64', 'value': spec.schema_b64},
                    {'name': 'SCHEMA_HASH', 'value': spec.schema_hash},
                    {'name': 'ELASTICSEARCH_URI', 'value': spec.elasticsearch_uri},
                    {'name': 'KAFKA_HOST', 'value': spec.kafka_host},
                    {'name': 'KAFKA_TOPIC', 'value': spec.kafka_topic},
                ]
            }
        ],
        containers=[
            {
                'name': 'consumer',
                'image': spec.image,
                'imagePullPolicy': 'IfNotPresent',
                'env': [
                    {'name': 'SCHEMA_B64', 'value': spec.schema_b64},
                    {'name': 'SCHEMA_HASH', 'value': spec.schema_hash},
                    {'name': 'ELASTICSEARCH_URI', 'value': spec.elasticsearch_uri},
                    {'name': 'KAFKA_HOST', 'value': spec.kafka_host},
                    {'name': 'KAFKA_TOPIC', 'value': spec.kafka_topic},
                ]
            }
        ],
        replicas=1
    )

    all_replica_sets = replica_sets.append(new_replica_set)

    new_job = Job(
        name=spec.service + '-schema-alias-switcher-' +
        random_generator(size=12),
        containers=[
            {
                'name': 'schema-monitor',
                'image': 'gcr.io/gt8-mindetic/consumer-tooling/scripts:2.0',
                'imagePullPolicy': 'Always',
                'args': ['swap_alias.py'],
                'env': [
                    {'name': 'SCHEMA_B64', 'value': spec.schema_b64},
                    {'name': 'SCHEMA_HASH', 'value': spec.schema_hash},
                    {'name': 'ELASTICSEARCH_URI', 'value': spec.elasticsearch_uri},
                    {'name': 'KAFKA_HOST', 'value': spec.kafka_host},
                    {'name': 'KAFKA_TOPIC', 'value': spec.kafka_topic},
                ]
            }
        ],
        annotations={
            'consumer.mindetic.gt8/schemaB64': spec.schema_b64
        }
    )

    # Ditch all old jobs and let metacontroller remove them. We only want one
    # alias switcher running when we launch a new replica set
    return {'replica_sets': all_replica_sets, 'jobs': [new_job]}


def update_active_replica_set(spec: CDCSpec, replica_sets: Iterable[ReplicaSet], jobs: Iterable[Job]):
    print("\n\n\nUPDATING ACTIVE\n\n\n", flush=True)

    # Update schema match with image
    for replica_set in replica_sets:
        if spec.schema_b64 == replica_set.schema_b64:
            replica_set.containers = [
                {
                    'name': 'consumer',
                    'image': spec.image,
                    'imagePullPolicy': 'IfNotPresent',
                    'env': [
                        {'name': 'SCHEMA_B64', 'value': spec.schema_b64},
                        {'name': 'SCHEMA_HASH', 'value': spec.schema_hash},
                        {'name': 'ELASTICSEARCH_URI',
                            'value': spec.elasticsearch_uri},
                        {'name': 'KAFKA_HOST', 'value': spec.kafka_host},
                        {'name': 'KAFKA_TOPIC', 'value': spec.kafka_topic},
                    ]
                }
            ]

    return {'replica_sets': replica_sets, 'jobs': jobs}


def promote_unactive_replica_set(spec: CDCSpec, replica_sets: Iterable[ReplicaSet], jobs: Iterable[Job]):
    print("\n\n\nPROMOTING INACTIVE\n\n\n", flush=True)

    # If not the replica_set for this schema, set unactive.
    # Promote if it is
    for replica_set in replica_sets:
        if spec.schema_b64 != replica_set.schema_b64:
            replica_set.set_unactive()
        else:
            replica_set.set_active()
            replica_set.containers = [
                {
                    'name': 'consumer',
                    'image': spec.image,
                    'imagePullPolicy': 'IfNotPresent',
                    'env': [
                        {'name': 'SCHEMA_B64', 'value': replica_set.schema_b64},
                        {'name': 'SCHEMA_HASH', 'value': replica_set.schema_hash},
                        {'name': 'ELASTICSEARCH_URI',
                            'value': spec.elasticsearch_uri},
                        {'name': 'KAFKA_HOST', 'value': spec.kafka_host},
                        {'name': 'KAFKA_TOPIC', 'value': spec.kafka_topic},
                    ]
                }
            ]

    new_job = Job(
        name=spec.service + '-schema-alias-switcher-' +
        random_generator(size=12),
        containers=[
            {
                'name': 'schema-monitor',
                'image': 'gcr.io/gt8-mindetic/consumer-tooling/scripts:2.0',
                'imagePullPolicy': 'Always',
                'args': ['swap_alias.py'],
                'env': [
                    {'name': 'SCHEMA_B64', 'value': spec.schema_b64},
                    {'name': 'SCHEMA_HASH', 'value': spec.schema_hash},
                    {'name': 'ELASTICSEARCH_URI', 'value': spec.elasticsearch_uri},
                    {'name': 'KAFKA_HOST', 'value': spec.kafka_host},
                    {'name': 'KAFKA_TOPIC', 'value': spec.kafka_topic},
                ]
            }
        ],
        annotations={
            'consumer.mindetic.gt8/schemaB64': spec.schema_b64
        }
    )

    # Ditch all old jobs and let metacontroller remove them. We only want one
    # alias switcher running when we switch schema
    jobs = [new_job]

    return {'replica_sets': replica_sets, 'jobs': jobs}


def random_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
