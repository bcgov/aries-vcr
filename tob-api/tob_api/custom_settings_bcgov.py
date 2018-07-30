'''
Enclose property names in double quotes in order to JSON serialize the contents in the API
'''
CUSTOMIZATIONS  = {
          "serializers":
          {
              "Location":
              {
                  "includeFields":[
                        "id",
                        "last_updated",
                        "credential",
                        "last_updated",
                        "addressee",
                        "civic_address",
                        "city",
                        "province",
                        "postal_code",
                        "country",
                        "type",
                        "issuer"
                    ]
              }
          }
}
         