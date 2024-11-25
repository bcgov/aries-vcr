topic_def_spec = {
    "type": "registration.registries.ca",
    "source_id": {"path": "$.credentialSubject.issuedTo.identifier"},
}

effective_date_credential_mapping_def_spec = {
    "name": "test_effective_date",
    "path": "$.validFrom",
}

expiry_date_credential_mapping_def_spec = {
    "name": "test_expiry_date",
    "path": "$.validUntil",
}

effective_date_mapping_def_spec = {
    **effective_date_credential_mapping_def_spec,
    "type": "effective_date",
}

expiry_date_mapping_def_spec = {
    **expiry_date_credential_mapping_def_spec,
    "type": "expiry_date",
}

issuer_def_spec = {
    "name": "issuer name",
    "did": "did:key:for:issuer",
    "abbreviation": "issuer abbrev",
    "email": "issuer email",
    "url": "issuer url",
    "endpoint": "issuer endpoint",
    "logo_b64": "issuer logo base64",
}

credential_type_def_spec = {
    "format": "vc_di",
    "schema": "BCPetroleum&NaturalGasTitle",
    "version": "1.0",
    "origin_did": issuer_def_spec.get("did"),
    "topic": topic_def_spec,
    "credential": {
        "effective_date": effective_date_credential_mapping_def_spec,
        "revoked_date": expiry_date_credential_mapping_def_spec,
    },
    "mappings": [
        effective_date_mapping_def_spec,
        expiry_date_mapping_def_spec,
    ],
    "cardinality": [
        {"path": "$.credentialSubject.issuedTo.id"},
    ],
}

credential_def_spec = {
    "format": "vc_di",
    "schema": credential_type_def_spec.get("schema"),
    "version": credential_type_def_spec.get("version"),
    "origin_did": credential_type_def_spec.get("origin_did"),
    "credential_id": "203296ac-6d8f-4988-9d7f-d23d3ca36db4",
    "raw_data": {
        "@context": ["https://www.w3.org/ns/credentials/v2"],
        "type": ["VerifiableCredential", "BCPetroleum&NaturalGasTitle"],
        "id": "https://orgbook.devops.gov.bc.ca/entities/A0131571/credentials/203296ac-6d8f-4988-9d7f-d23d3ca36db4",
        "issuer": {
            "id": "did:web:untp.traceability.site:parties:regulators:director-of-petroleum-lands"
        },
        "validFrom": "2024-08-12T05:44:20+00:00",
        "validUntil": "2025-08-12T05:44:20+00:00",
        "credentialSubject": {
            "issuedTo": {
                "id": "https://orgbook.gov.bc.ca/entity/A0131571",
                "legalName": "PACIFIC CANBRIAM ENERGY LIMITED",
                "identifier": "A0131571",
            }
        },
        "proof": [
            {
                "type": "DataIntegrityProof",
                "cryptosuite": "eddsa-jcs-2022",
                "verificationMethod": "did:web:untp.traceability.site:parties:regulators:director-of-petroleum-lands#multikey",
                "proofPurpose": "assertionMethod",
                "proofValue": "z2Nr9eDUfBzircv484R3u7vzdxARh5D8vsbj4ohFRQZhkq2PTdJ9YsLfF18mafaPMtchV5EefmovvFoFbFNmLqrWW",
            }
        ],
    },
}
