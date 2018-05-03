# from kubernetes.client import ApiClient
# from kubernetes.client.models.v1_replica_set import V1ReplicaSet
# from kubernetes.client.models.v1_replica_set_spec import V1ReplicaSetSpec
# from kubernetes.client.models.v1_label_selector import V1LabelSelector
# from kubernetes.client.models.v1_pod_template_spec import V1PodTemplateSpec
# from kubernetes.client.models.v1_pod_spec import V1PodSpec
# from kubernetes.client.models.v1_container import V1Container
# from watch import handle

# import json
# import os
# import sys


# def test_same_schema_exists():
#     __location__ = os.path.realpath(os.path.join(
#         os.getcwd(), os.path.dirname(__file__)))

#     api = ApiClient()

#     with open(__location__ + '/same_schema_exists.json') as test_payload:
#         payload = json.load(test_payload)
#         parent = payload['parent']
#         children = payload['children']

#         updated_spec = handle(parent, children)

#         print(json.dumps(updated_spec))
#         print("-----")
#         print(json.dumps(children))
#         sys.stdout.flush()

#         assert {'children': children} == updated_spec
