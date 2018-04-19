import jsonschema
import logging

from api.models.IssuerService import IssuerService
from api.models.Jurisdiction import Jurisdiction
from api.models.VerifiableClaimType import VerifiableClaimType


ISSUER_JSON_SCHEMA = {
  '$schema': 'http://json-schema.org/draft-04/schema',
  'type': 'object',
  'properties': {
    'issuer': {
      'type': 'object',
      'properties': {
        'did': {'type': 'string', 'minLength': 1}, # check length + valid characters?
        'name': {'type': 'string', 'minLength': 1},
        'abbreviation': {'type': 'string'},
        'endpoint': {'type': 'string'}
      },
      'required': ['did', 'name']
    },
    'jurisdiction': {
      'type': 'object',
      'properties': {
        'name': {'type': 'string', 'minLength': 1},
        'abbreviation': {'type': 'string'}
      },
      'required': ['name']
    },
    'claim-types': {
      'type': 'array',
      'items': {
        'type': 'object',
        'properties': {
          'name': {'type': 'string', 'minLength': 1},
          'schema': {'type': 'string', 'minLength': 1},
          'version': {'type': 'string', 'minLength': 1},
          'endpoint': {'type': 'string'}
        },
        'required': ['name', 'schema', 'version']
      }
    }
  },
  'required': ['issuer', 'jurisdiction']
}


class IssuerManager:
  """
  Handle registration of issuer services, taking the JSON definition
  of the issuer and updating the related tables.
  """
  
  def __init__(self):
    self.__logger = logging.getLogger(__name__)
  

  def registerIssuer(self, spec):
    jsonschema.validate(spec, ISSUER_JSON_SCHEMA)

    jurisdiction = self.checkUpdateJurisdiction(spec['jurisdiction'])
    issuer = self.checkUpdateIssuerService(jurisdiction, spec['issuer'])
    ctypes = self.checkUpdateClaimTypes(issuer, spec.get('claim-types', []))
    
    result = {
      'jurisdiction': {
        'id': jurisdiction.id,
        'name': jurisdiction.name,
        'abbreviation': jurisdiction.abbrv
      },
      'issuer': {
        'id': issuer.id,
        'did': issuer.DID,
        'name': issuer.name,
        'abbreviation': issuer.issuerOrgTLA,
        'endpoint': issuer.issuerOrgURL
      },
      'claim-types': [
        {
          'id': ctype.id,
          'name': ctype.claimType,
          'schema': ctype.schemaName,
          'version': ctype.schemaVersion,
          'endpoint': ctype.issuerURL
        } for ctype in ctypes
      ]
    }
    return result
    

  def updateRecord(self, record, spec):
    update = False
    for field, value in spec.items():
      old = getattr(record, field, None)
      if old != value:
        setattr(record, field, value)
        update = True
    if update:
      record.save()
    return record


  def checkUpdateJurisdiction(self, jurisd_def):
    jurisd_name = jurisd_def['name'].strip()
    jurisd_abbr = jurisd_def.get('abbreviation', '').strip() or None
    jurisdiction = Jurisdiction.objects.filter(name=jurisd_name)
    if not jurisdiction:
      self.__logger.debug("Jurisdiction '{0}' does not exist.  Creating ...".format(jurisd_name))
      jurisdiction = Jurisdiction(
        abbrv=jurisd_abbr,
        name=jurisd_name,
        displayOrder=0,
        isOnCommonList=True
      )
      jurisdiction.save()
    else:
      jurisdiction = self.updateRecord(jurisdiction[0], {'abbrv': jurisd_abbr})
    return jurisdiction


  def checkUpdateIssuerService(self, jurisdiction, issuer_def):
    issuer_did = issuer_def['did'].strip()
    issuer_name = issuer_def['name'].strip()
    issuer_abbr = issuer_def.get('abbreviation', '').strip() or None
    issuer_url = issuer_def.get('endpoint', '').strip() or None
    
    # search by DID
    issuer = IssuerService.objects.filter(DID=issuer_did)
    if not issuer:
      # search by name
      issuer = IssuerService.objects.filter(name=issuer_name)
    if not issuer:
      self.__logger.debug("Issuer service '{0}' does not exist.  Creating ...".format(issuer_name))
      issuer = IssuerService(
                name=issuer_name,
                DID=issuer_did,
                issuerOrgTLA=issuer_abbr,
                issuerOrgURL=issuer_url,
                jurisdictionId=jurisdiction
      )
      issuer.save()
    else:
      issuer = self.updateRecord(issuer[0], {
        'name': issuer_name,
        'DID': issuer_did,
        'issuerOrgTLA': issuer_abbr,
        'issuerOrgURL': issuer_url,
        'jurisdictionId': jurisdiction
      })
    return issuer


  def checkUpdateClaimTypes(self, issuer, type_defs):
    claim_types = VerifiableClaimType.objects.filter(issuerServiceId=issuer)
    exist_by_schema = {}
    for ctype in claim_types:
      skey = '{}:{}'.format(ctype.schemaName, ctype.schemaVersion)
      exist_by_schema[skey] = ctype
    results = []
    
    for type_def in type_defs:
      type_name = type_def['name']
      type_schema = type_def['schema']
      type_version = type_def['version']
      type_endpoint = type_def.get('endpoint', '').strip() or None
    
      skey = '{}:{}'.format(type_schema, type_version)
      if skey in exist_by_schema:
        claimtype = self.updateRecord(exist_by_schema[skey], {
          'claimType': type_name,
          'issuerURL': type_endpoint
        })
      else:
        self.__logger.debug("Claim type '{0}' does not exist.  Creating ...".format(type_name))
        claimtype = VerifiableClaimType(
          claimType=type_name,
          issuerServiceId=issuer,
          issuerURL=type_endpoint,
          schemaName=type_schema,
          schemaVersion=type_version
        )
        claimtype.save()
      results.append(claimtype)
    
    # clean up existing records
    for ctype in exist_by_schema.values():
      if ctype not in results:
        ctype.delete()
    
    return results
