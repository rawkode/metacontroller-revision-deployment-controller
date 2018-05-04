from cdc import CDCSpec
from hashlib import sha256


def test_cdc_spec():
    cds = CDCSpec(
        service='service',
        image='image:latest',
        elasticsearch_uri='http://elasticsearch:9200',
        kafka_host='kafka',
        kafka_topic='topic',
        schema_b64='e30k',
        schema_alias='myalias',
        support_schemas=4
    )

    assert cds.schema_hash == sha256('e30k'.encode('utf-8')).hexdigest()

    assert cds.service == 'service'
    assert cds.image == 'image:latest'
    assert cds.elasticsearch_uri == 'http://elasticsearch:9200'
    assert cds.kafka_host == 'kafka'
    assert cds.kafka_topic == 'topic'
    assert cds.schema_b64 == 'e30k'
    assert cds.schema_alias == 'myalias'
    assert cds.support_schemas == 4