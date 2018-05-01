from utils import request_in_to_objects

import json
import os


def test_initial_payload():
    __location__ = os.path.realpath(os.path.join(
        os.getcwd(), os.path.dirname(__file__)))

    with open(__location__ + '/payloads/initial_request.json') as test_payload:
        json_object = json.load(test_payload)
        objects = request_in_to_objects(json_object)

        assert [] == objects


def test_same_schema_payload():
    __location__ = os.path.realpath(os.path.join(
        os.getcwd(), os.path.dirname(__file__)))

    with open(__location__ + '/payloads/schema_exists_different_image.json') as test_payload:
        json_object = json.load(test_payload)
        objects = request_in_to_objects(json_object)

        expected_objects = [{
            'type': 'ReplicaSet.extensions/v1beta1',
            'name': 'user-service-consumer-9fkdl',
            'replicas': 1,
            'annotations': {
                'consumer.mindetic.gt8/schemaB64': 'e30K'
            },
            'containers': [
                {
                    'name': 'consumer',
                    'image': 'nginx:latest'
                }
            ]
        }]

        assert expected_objects == objects
