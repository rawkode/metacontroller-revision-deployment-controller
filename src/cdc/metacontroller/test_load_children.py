from cdc.metacontroller import load_children

import json
import os


def test_load_children():
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

    children_dict = json.load(open(__location__ + '/test_children.json'))
    children = load_children(payload=children_dict)

    assert 'replica_sets' in children
    assert len(children['replica_sets']) == 1

    assert 'jobs' in children
    assert len(children['jobs']) == 0
