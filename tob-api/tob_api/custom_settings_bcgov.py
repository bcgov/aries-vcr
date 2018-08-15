"""
Enclose property names in double quotes in order to JSON serialize the contents in the API
"""
CUSTOMIZATIONS = {
    "serializers": {
        "Address": {
            "includeFields": [
                "id",
                "create_timestamp",
                "update_timestamp",
                "addressee",
                "civic_address",
                "city",
                "province",
                "postal_code",
                "country",
                "credential"
            ]
        }
    }
}
