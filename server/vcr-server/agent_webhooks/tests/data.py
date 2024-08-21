topic_def_spec = {
    "type": "registration.registries.ca",
    "source_id": {"path": "$.path.to.topic.source_id"},
}

effective_date_credential_mapping_def_spec = {
    "name": "test_effective_date",
    "path": "$.path.to.credential.effective_date",
}

revoked_date_credential_mapping_def_spec = {
    "name": "test_expiry_date",
    "path": "$.path.to.credential.revoked_date",
}

effective_date_mapping_def_spec = {
    **effective_date_credential_mapping_def_spec,
    "type": "effective_date",
}

revoked_date_mapping_def_spec = {
    **revoked_date_credential_mapping_def_spec,
    "type": "revoked_date",
}

credential_type_def_spec = {
    "format": "vc_di",
    "schema": "BCPetroleum&NaturalGasTitle",
    "version": "1.0",
    "origin_did": "did:key:for:issuer",
    "topic": topic_def_spec,
    "credential": {
        "effective_date": effective_date_credential_mapping_def_spec,
        "revoked_date": revoked_date_credential_mapping_def_spec,
    },
    "mappings": [
        effective_date_mapping_def_spec,
        revoked_date_mapping_def_spec,
    ],
}

issuer_def_spec = {
    "name": "issuer name",
    "did": credential_type_def_spec.get("origin_did"),
    "abbreviation": "issuer abbrev",
    "email": "issuer email",
    "url": "issuer url",
    "endpoint": "issuer endpoint",
    "logo_b64": "issuer logo base64",
}
