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


# def test_same_schema_image_change():
#     __location__ = os.path.realpath(os.path.join(
#         os.getcwd(), os.path.dirname(__file__)))

#     api = ApiClient()

#     with open(__location__ + '/same_schema_image_change.json') as test_payload:
#         payload = json.load(test_payload)
#         parent = payload['parent']
#         children = payload['children']

#         new_spec = handle(parent, children)

#         assert new_spec['children']['ReplicaSet.extensions/v1beta1']['user-service-consumer-9fkdl']['spec']['template']['spec']['containers'][0]['image'] == 'nginx:new'
