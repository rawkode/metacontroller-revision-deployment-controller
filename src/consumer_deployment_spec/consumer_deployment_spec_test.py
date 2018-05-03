from consumer_deployment_spec import ConsumerDeploymentSpec
from hashlib import sha256


def test_spec():
    cds = ConsumerDeploymentSpec(
        service='service',
        image='image:latest',
        elasticsearch_uri='http://elasticsearch:9200',
        schema_b64='e30k',
        schema_alias='myalias',
        support_schemas=4
    )

    assert cds.schema_hash == sha256('e30k'.encode('utf-8')).hexdigest()

    assert cds.service == 'service'
    assert cds.image == 'image:latest'
    assert cds.elasticsearch_uri == 'http://elasticsearch:9200'
    assert cds.schema_b64 == 'e30k'
    assert cds.schema_alias == 'myalias'
    assert cds.support_schemas == 4
