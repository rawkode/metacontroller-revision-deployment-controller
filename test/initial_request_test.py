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


# def test_initial_request():
#     __location__ = os.path.realpath(os.path.join(
#         os.getcwd(), os.path.dirname(__file__)))

#     api = ApiClient()

#     with open(__location__ + '/initial_request.json') as test_payload:
#         payload = json.load(test_payload)
#         parent = payload['parent']
#         children = payload['children']

#         assert handle(parent, children) == api.sanitize_for_serialization({
#             'children': [
#                 V1ReplicaSet(
#                     api_version='apps/v1',
#                     kind='ReplicaSet',
#                     metadata={
#                         'generateName': parent['spec']['service'] + '-consumer-',
#                         'annotations': {
#                             'consumer.mindetic.gt8/schemaB64': parent['spec']['schemaB64']
#                         }
#                     },
#                     spec=V1ReplicaSetSpec(
#                         replicas=parent['spec']['replicas'],
#                         selector=V1LabelSelector(
#                             match_labels={
#                                 'service': parent['spec']['service'],
#                                 'component': 'consumer'
#                             }),
#                         template=V1PodTemplateSpec(
#                             metadata={
#                                 'labels': {
#                                     'service': parent['spec']['service'],
#                                     'component': 'consumer'
#                                 }
#                             },
#                             spec=V1PodSpec(
#                                 containers=[
#                                     V1Container(
#                                         name='consumer',
#                                         image=parent['spec']['image']
#                                     )
#                                 ]
#                             )
#                         )
#                     )
#                 )
#             ]
#         })
