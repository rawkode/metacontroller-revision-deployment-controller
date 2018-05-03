from consumer_deployment_spec import ConsumerDeploymentSpec
from flask import Flask, request, jsonify
from kubernetes.client import ApiClient
from kubernetes.client.models.v1_container import V1Container
from kubernetes.client.models.v1_label_selector import V1LabelSelector
from kubernetes.client.models.v1_pod_spec import V1PodSpec
from kubernetes.client.models.v1_pod_template_spec import V1PodTemplateSpec
from kubernetes.client.models.v1_replica_set import V1ReplicaSet
from kubernetes.client.models.v1_replica_set_spec import V1ReplicaSetSpec
from utils import objects_to_request_out, request_in_to_objects, new_replica_set


import copy
import datetime
import json
import logging
import pprint
import sys
import time
import uuid

app = Flask(__name__)


@app.route('/watch', methods=['POST'])
def watch():
    json_payload = request.get_json()

    print("Request")
    print("Parent")
    print(json_payload['parent'])
    print("Children")
    print(json.dumps(json_payload['children']))
    sys.stdout.flush()

    print('Response')
    response = handle(json_payload)
    print(json.dumps(response))
    sys.stdout.flush()

    time.sleep(1)

    return jsonify(response), 200


def does_replica_set_exist_for_schema(schemaB64, objects):
    for object in objects:
        if object['annotations']['consumer.mindetic.gt8/schemaB64'] == schemaB64:
            return object['name']
    return None


def handle(payload):
    objects = request_in_to_objects(payload)

    print("Loaded Current Objects")
    print(objects)
    sys.stdout.flush()

    parent_spec = payload['parent']['spec']

    consumer_deployment_spec = ConsumerDeploymentSpec(
        service=parent_spec['service'],
        image=parent_spec['image'],
        schema_b64=parent_spec['schemaB64'],
        elasticsearch_uri=parent_spec['elasticsearchUri'],
        schema_alias=parent_spec['schemaAlias'],
        support_schemas=parent_spec['supportSchemas']
    )

    replica_set = does_replica_set_exist_for_schema(
        consumer_deployment_spec.schema_b64, objects)

    if replica_set is None:
        print('Creating consumer for ' + consumer_deployment_spec.service +
              ' with schemaB64 ' + consumer_deployment_spec.schema_b64)
        sys.stdout.flush()

        for object in objects:
            object['annotations'].pop(
                'consumer.mindetic.gt8/active', None)

        new = [{'type': 'ReplicaSet.extensions/v1beta1'}] + objects

        return objects_to_request_out(consumer_deployment_spec, new)

    for object in objects:
        print('Comparing ' + replica_set + ' with ' + object['name'])
        sys.stdout.flush()

        if replica_set == object['name']:
            if 'consumer.mindetic.gt8/active' in object['annotations']:
                if object['image'] == consumer_deployment_spec.image:
                    # No update
                    return objects_to_request_out(consumer_deployment_spec, objects)
                else:
                    print("Potentially updating image from " +
                          object['image'] + ' to ' + consumer_deployment_spec.image)
                    object['annotations']['consumer.mindetic.gt8/active'] = str(
                        datetime.datetime.now())
                    object['image'] = consumer_deployment_spec.image

                    return objects_to_request_out(consumer_deployment_spec, objects)

    # Looks like we're rolling back
    for object in objects:
        if replica_set == object['name']:
            print("Potentially rolling back to schema " + consumer_deployment_spec.schema_b64
                  + ' from image ' + object['image'] + ' to ' + consumer_deployment_spec.image)
            sys.stdout.flush()
            object['annotations']['consumer.mindetic.gt8/active'] = str(
                datetime.datetime.now())
            object['image'] = consumer_deployment_spec.image
        else:
            object['annotations'].pop(
                'consumer.mindetic.gt8/active', None)

    return objects_to_request_out(consumer_deployment_spec, objects)
