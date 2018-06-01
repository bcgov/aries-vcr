CREDENTIAL_OFFER_JSON_SCHEMA = {
    # TODO: use newer draft of spec?
    "$schema": "http://json-schema.org/draft-04/schema",
    "type": "object",
    # TODO: Flesh out definitions further?
    "properties": {
        "credential-offer": {"type": "object"},
        "credential-definition": {"type": "object"},
    },
    "required": ["credential-offer", "credential-definition"],
}
