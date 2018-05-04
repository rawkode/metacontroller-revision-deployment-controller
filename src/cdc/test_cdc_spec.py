from cdc import CDCSpec
from hashlib import sha256


def test_cdc_spec():
    cds = CDCSpec(
        service='service',
        image='image:latest',
        schema_b64='e30k',
        schema_alias='myalias',
        support_schemas=4
    )

    assert cds.schema_hash == sha256('e30k'.encode('utf-8')).hexdigest()

    assert cds.service == 'service'
    assert cds.image == 'image:latest'
    assert cds.schema_b64 == 'e30k'
    assert cds.schema_alias == 'myalias'
    assert cds.support_schemas == 4
