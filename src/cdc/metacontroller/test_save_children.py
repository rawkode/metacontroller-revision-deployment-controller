from cdc import CDCSpec
from cdc.metacontroller import save_children
from cdc.metacontroller.test_utils import get_new_replica_set, get_replica_set, get_spec
from cdc.replica_set import ReplicaSet
from datetime import datetime

import kubernetes.client.models as k8s


def test_save_children():
    spec = get_spec()
    replica_sets = [get_new_replica_set(), get_replica_set()]

    response = save_children(spec, {'replica_sets': replica_sets})

    assert 'children' in response

    children = response['children']

    assert len(children) == 2
