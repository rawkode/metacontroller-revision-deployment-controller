from cdc.metacontroller import load_replica_set

import json
import os


def test_load_replica_set():
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

    replica_set_dict = json.load(open(__location__ + '/test_replica_set.json'))
    replica_set = load_replica_set(payload=replica_set_dict)

    assert replica_set.name == 'user-service-consumer-9fkdl'


def test_load_replica_set_no_name():
    payload = {
        'whatever': None
    }

    replica_set = load_replica_set(payload=payload)

    assert replica_set == None
