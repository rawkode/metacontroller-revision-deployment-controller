from cdc.metacontroller import load_parent

import json
import os


def test_load_parent():
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

    parent_dict = json.load(open(__location__ + '/test_parent.json'))
    parent = load_parent(payload=parent_dict)

    assert parent.service == 'user-service'
    assert parent.image == 'nginx:latest'
    assert parent.schema_b64 == 'e30k'
    assert parent.kafka_host == 'kafka'
    assert parent.kafka_topic == 'topic'
    assert parent.schema_alias == 'primary_schema_alias'
    assert parent.elasticsearch_uri == 'http://elasticsearch:9200'
    assert parent.support_schemas == 3
