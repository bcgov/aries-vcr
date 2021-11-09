### Changes to Aries-vcr issuer schema

The Aries-vcr application is undergoing changes to enhance user experience on applications such as Orgbook. The primary change to the Aries-vcr application is in the way that credential schemas are issued.  
  
Included below are a list of optional changes to credential schemas that issuers may be interested in making. For the purpose of clearly displaying how these changes are being used, we've provided examples of the credential changes in the new Orgbook site.

#### Credential title
The credential title is the main attribute you want users to see when viewing a credential. An example of this would be the business number of a business number credential. See figure 1 for an example.

![](./assets/schema_label_cred_title.png)  
*Figure 1: Schema label and credential title*
  
#### Highlighted attributes
Highlighted attributes are secondary credential attributes that you believe would be important to a user viewing a specific credential. An example of this would be a Cannabis marketing license credential. A user would likely be interested in knowing the effective and expiry date of the credential, but probably would not care much about the issue date since it does not have anything to do with the validity of the credential. Aries-vcr allows issuers to include only relevant credential attributes in their credential displays. See figure 2 for an example.  

![](./assets/highlighted_attributes.png)  
*Figure 2: Highlighted attributes*

#### Schema labels
Aries-vcr has added the functionality to specify the name of a credential schema in a multilingual format. These schema names appear as the title of the credential and let users know what type of credential they are viewing. This schema label is optional and is only needed if you plan on supporting multi language use. If no schema label is defined, a good fallback is to use the credential type description displayed in the same way as a schema label. The new version of Orgbook takes this approach. See figure 1 for example of a schema label in Orgbook.
  
#### Aries-vcr defaults
##### Credential title:
If the credential title is not specified in a credential schema, or there is no claim label to match the credential title, then applications such as Orgbook may instead use the registration number of the entity holding the credential. See figure 3 for an example  
![](./assets/default_cred_title.png)  
*Figure 3: default credential title and highlighted attributes*
  
##### Highlighted attributes:
If no highlighted attributes are specified, or there are no claim labels to match the highlighted attributes, then applications like Orgbook will not display any highlighted attributes. See figure 3.1 to see how a credential with no highlighted attributes or credential title is displayed.  
![](./assets/default_highlighted.png)  
*Figure 3.1: Default credential title and highlighted attributes*

#### Recommended changes to schema
To incorporate these optional changes, Aries-vcr recommends reviewing the new schema attributes and how to add them to your credential schema in the section below.

~~~
{
  "schema_name": "registration.registries.ca",
  "schema_version": "1.0.44",
  "attributes": [
    "registration_id",
    "registration_date",
    ...
    "reason_description",
    "expiry_date"
  ],
  "metadata": {
    "topic": [
      {
        "name": "registration_id",
        "topic_type": "registration.registries.ca"
      }
    ],
    "highlighted_attributes":[
        "reason_description"
      ],
    "credential_title":"registration_id",
    "cardinality": [
      "registration_id"
    ],
    "date_fields": {
      "effective_date": "effective_date",
      "revoked_date": "expiry_date",
      "other_date_fields": [
        "registration_date",
        "entity_name_effective",
        "entity_name_assumed_effective",
        "entity_status_effective"
      ]
    },
    "address_fields": [],
    "search_fields": [
      "registration_id",
      "entity_name"
    ],
    "labels": {
      "schema": {
        "en": "Registration Credential"
      },
      "schema_description":{
      	"en": "Registration Description"
      },
      "attributes": [
        {
          "name": "registration_id",
          "translations": {
            "en": {
              "label": "Registration ID",
              "description": "Registration/Incorporation Number or Identifying Number"
            }
          }
        },
		
        ...
		
        {
          "name": "reason_description",
          "translations": {
            "en": {
              "label": "DEMO",
              "description": "Reason for credential issue/update"
            }
          }
        },
        {
          "name": "expiry_date",
          "translations": {
            "en": {
              "label": "Credential Expiry Date",
              "description": "Date Credential expired"
            }
          }
        }
      ]
    }
  }
}
~~~
*Figure 4: Example registration schema*

##### Setting the schema label:
In order to set the schema label add the following JSON object to `metadata->labels`
~~~
"schema": {
	"en": "<YOUR SCHEMA NAME, Example: Registration >"
},
"schema_description":{
	"en": "<YOUR SCHEMA DESCRIPTION, Example: Credential proving an entity's registration>"
},
~~~


##### Setting the credential title and highlighted attributes:
To set the credential title and highlighted attributes add the following JSON object to `metadata`:
~~~
"highlighted_attributes":[
	"<YOUR HIGHLIGHTED ATTRIBUTE KEY 1>",
	"<YOUR HIGHLIGHTED ATTRIBUTE KEY 2>"
  ],
"credential_title":"<YOUR CREDENTIAL TITLE KEY>",
~~~
highlighted attribute keys and the credential title key refer to the attribute names on each of the attributes in the schema. An example is shown in figure 4.1. Highlighted attributes will appear on credential cards in the order they're listed on the schema. Example: attribute #1 will appear above attribute #2 on this credential card.

![](./assets/attribute_key.png)
*Figure 4.1: Example attribute key*

##### Setting the credential title and highlighted attribute labels:
Attribute labels appear to the left of an attribute value on a credential card. The attribute label describes the attribute value being displayed on the credential card. See figure 4.2 for an example.

![](./assets/attribute_label_value.png)
*Figure 4.2: Attribute label and value*

To set the attribute label simply edit the claim label for the attribute in question. To do so, in `metadata->labels->attributes->translations->[locale]->label` change the `name` field to your desired label as seen in figure 4.3 where we change the `reason_description` from `Reason` to `DEMO`. See figure 4.4 for the resulting change in Orgbook

![](./assets/reason_to_demo.png)  
*Figure 4.3: Change from reason to demo*

![](./assets/reason_to_demo_result.png)  
*Figure 4.4: resulting change in Orgbook*





