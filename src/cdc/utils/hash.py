from hashlib import sha256


def hash_schema(schema_b64: str):
    return sha256(schema_b64.encode('utf-8')).hexdigest()
