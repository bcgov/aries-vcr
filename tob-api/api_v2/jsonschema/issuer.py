ISSUER_JSON_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema",
    "type": "object",
    "properties": {
        "issuer": {
            "type": "object",
            "properties": {
                # check length + valid characters?
                "did": {"type": "string", "minLength": 1},
                "name": {"type": "string", "minLength": 1},
                "abbreviation": {"type": "string"},
                "email": {"type": "string", "minLength": 1},
                "url": {"type": "string"},
            },
            "required": ["did", "name"],
        },
        "credential_types": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "schema": {"type": "string", "minLength": 1},
                    "version": {"type": "string", "minLength": 1},
                    "description": {"type": "string", "minLength": 1},
                    "endpoint": {"type": "string"},
                    "mapping": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "from": {
                                    "type": "string",
                                    "enum": ["claim", "value"],
                                },
                                "input": {"type": "string"},
                                "processor": {
                                    "type": "array",
                                    # TODO: dynamically set restrictions on
                                    # available functions based on contents
                                    # of processor directory?
                                    "items": {"type": "string"},
                                },
                            },
                        },
                    },
                },
                "required": ["name", "schema", "version"],
            },
        },
    },
    "required": ["issuer"],
}
