let mockOrgs = {};
mockOrgs[1] = {
  "id": 1,
  "busId": "..",
  "orgType": {
    "id": 1,
    "theType": "corp",
    "description": "Corporation",
    "effectiveDate": "2017-10-05",
    "expirationDate": "2017-10-05"
  },
  "jurisdictionId": {
    "id": 1,
    "jurisdictionAbbrv": "..",
    "jurisdictionName": "..",
    "displayOrder": 1,
    "isOnCommonList": true,
    "effectiveDate": "2017-10-05",
    "expirationDate": "2017-10-05"
  },
  "LegalName": "Sprockets & Widgets Inc.",
  "primaryLocation": {
    "id": 1,
    "voLocationTypeId": {
      "id": 0,
      "theType": "civic_address",
      "description": "Civic Address",
      "effectiveDate": "2017-10-05",
      "expirationDate": "2017-10-05",
      "displayOrder": 0
    },
    "addressee": "",
    "addlDeliveryInfo": "",
    "unitNumber": "",
    "streetAddress": "130 Future Rd",
    "municipality": "Vernon",
    "province": "BC",
    "postalCode": "V0A 0A0",
    "latLong": ""
  },
  "effectiveDate": "2017-10-05",
  "endDate": "2017-10-05"
}
mockOrgs[2] = {
  "id": 2,
  "busId": "..",
  "orgType": {
    "id": 1,
    "theType": "corp",
    "description": "Corporation",
    "effectiveDate": "2017-10-05",
    "expirationDate": "2017-10-05",
    "displayOrder": 0
  },
  "jurisdictionId": {
    "id": 1,
    "jurisdictionAbbrv": "..",
    "jurisdictionName": "..",
    "displayOrder": 1,
    "isOnCommonList": true,
    "effectiveDate": "2017-10-05",
    "expirationDate": "2017-10-05"
  },
  "LegalName": "Alternative Data Intl.",
  "primaryLocation": {
    "id": 1,
    "voLocationTypeId": {
      "id": 1,
      "theType": "civic_address",
      "description": "Civic Address",
      "effectiveDate": "2017-10-05",
      "expirationDate": "2017-10-05",
      "displayOrder": 0
    },
    "addressee": "",
    "addlDeliveryInfo": "",
    "unitNumber": "",
    "streetAddress": "1428 Elm St",
    "municipality": "100 Mile House",
    "province": "BC",
    "postalCode": "V0A 0A0",
    "latLong": ""
  },
  "effectiveDate": "2017-10-05",
  "endDate": "2017-10-05"
}


export class MockData {
  fetchRecord (moduleId, recordId) {
    let src = null;
    if(moduleId === 'verifiedorgs')
      src = mockOrgs;
    if(src)
      return src[recordId];
  }
};
