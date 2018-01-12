from api.indy.claimParser import ClaimParser
from api.exceptions.ClaimTypeNotRegisteredException import ClaimTypeNotRegisteredException
from api.exceptions.OrganizationNotRegisteredException import OrganizationNotRegisteredException
from api.models.DoingBusinessAs import DoingBusinessAs
from api.models.Location import Location
from api.models.LocationType import LocationType
from rest_framework.exceptions import APIException
from api.indy.agent import Agent
from django.utils import timezone
from api.models.VerifiableClaimType import VerifiableClaimType
from api.models.IssuerService import IssuerService
from api.models.VerifiableClaim import VerifiableClaim
import logging
import base64
from api.models.Jurisdiction import Jurisdiction
from api.models.VerifiableOrgType import VerifiableOrgType
from api.models.VerifiableOrg import VerifiableOrg
from api.indy import eventloop
import datetime

# ToDo:
# * The code is currently making assumtions in order to fill in gaps in the infomration provided with a claim.
class ClaimProcesser(object):
    """
    Parses and processes a claim.
    """

    def __init__(self) -> None:
      self.__orgbook = Agent()
      self.__logger = logging.getLogger(__name__)
    
    def __ToDateTime(self, timeStamp: str):
      dateTime = None
      if timeStamp: 
        try:
          dateTime = datetime.datetime.utcfromtimestamp(int(timeStamp))
        except:
          pass

      return dateTime
      
    def __get_VerifiableClaimType(self, claim: ClaimParser):
      # VerifiableClaimTypes are registered by issuers.
      # If the VerifiableClaimType has not been registered we can't accept the claim.
      verifiableClaimTypeName = claim.claimType
      
      verifiableClaimType = VerifiableClaimType.objects.filter(claimType=verifiableClaimTypeName)
      if not verifiableClaimType:
        self.__logger.warn("VerifiableClaimType, {0}, has not been registered ...".format(verifiableClaimTypeName))
      else:
        self.__logger.debug("VerifiableClaimType, {0}, exists ...".format(verifiableClaimTypeName))
        verifiableClaimType = verifiableClaimType[0]
      
      return verifiableClaimType

    def __get_VerifiableOrg(self, claim: ClaimParser):
      name = claim.getField("legal_name")
      organizationId = claim.getField("legal_entity_id")

      verifiableOrg = VerifiableOrg.objects.filter(orgId=organizationId)
      if not verifiableOrg:
        self.__logger.debug("Organization, {0}, with business id {1} does not exist.".format(name, organizationId))
      else:
        self.__logger.debug("Organization, {0}, with business id {1} exists.".format(name, organizationId))
        verifiableOrg = verifiableOrg[0]

      return verifiableOrg

    def __get_VerifiableOrgType(self, claim: ClaimParser):
      orgTypeCode = claim.getField("org_type")
      
      verifiableOrgType = VerifiableOrgType.objects.filter(orgType=orgTypeCode)      
      if not verifiableOrgType:
        self.__logger.debug("VerifiableOrgType, {0}, does not exist.  Creating ...".format(orgTypeCode))
        verifiableOrgType = VerifiableOrgType(
          orgType = orgTypeCode,
          description = orgTypeCode,
          displayOrder = 0          
        )
        verifiableOrgType.save()
      else:
        self.__logger.debug("VerifiableOrgType, {0}, exists ...".format(orgTypeCode))
        verifiableOrgType = verifiableOrgType[0]
      
      return verifiableOrgType

    def __get_Jurisdiction(self, claim: ClaimParser):
      jurisdictionName = claim.getField("city")
      
      jurisdiction = Jurisdiction.objects.filter(name=jurisdictionName)
      if not jurisdiction:
        self.__logger.debug("Jurisdiction, {0}, does not exist.  Creating ...".format(jurisdictionName))
        jurisdiction = Jurisdiction(
          abbrv = jurisdictionName,
          name = jurisdictionName,
          displayOrder = 0,
          isOnCommonList = True
        )
        jurisdiction.save()
      else:
        self.__logger.debug("Jurisdiction, {0}, exists ...".format(jurisdictionName))
        jurisdiction = jurisdiction[0]
      
      return jurisdiction

    def __get_LocationType(self, locationTypeName: str):
      
      locationType = LocationType.objects.filter(locType=locationTypeName)
      if not locationType:
        self.__logger.debug("LocationType, {0}, does not exist.  Creating ...".format(locationTypeName))
        locationType = LocationType(
          locType = locationTypeName,
          description = locationTypeName,
          displayOrder = 0
        )
        locationType.save()
      else:
        self.__logger.debug("LocationType, {0}, exists ...".format(locationTypeName))
        locationType = locationType[0]
      
      return locationType

    def __CreateOrUpdateVerifiableOrg(self, claim: ClaimParser, verifiableOrg: VerifiableOrg):
      organizationId = claim.getField("legal_entity_id")
      name = claim.getField("legal_name")
      effectiveDate = self.__ToDateTime(claim.getField("effective_date"))
      endDate = endDate = self.__ToDateTime(claim.getField("end_date"))

      orgType = self.__get_VerifiableOrgType(claim)
      jurisdiction = self.__get_Jurisdiction(claim)

      if not verifiableOrg:
        self.__logger.debug("Registering {0} ...".format(name))
        verifiableOrg = VerifiableOrg(
          orgId = organizationId,
          orgTypeId = orgType,
          jurisdictionId = jurisdiction,
          legalName = name,
          effectiveDate = effectiveDate,
          endDate = endDate
        )
        verifiableOrg.save()
      else:
        self.__logger.debug("Updating records for {0} ... ".format(name))
        verifiableOrg.orgId = organizationId
        verifiableOrg.orgTypeId = orgType
        verifiableOrg.jurisdictionId = jurisdiction
        verifiableOrg.legalName = name
        verifiableOrg.effectiveDate = effectiveDate
        verifiableOrg.endDate = endDate
        verifiableOrg.save()

      return verifiableOrg

    def __CreateOrUpdateDoingBusinessAs(self, claim: ClaimParser, verifiableOrg: VerifiableOrg):
      dbaName = claim.getField("doing_business_as_name")
      effectiveDate = self.__ToDateTime(claim.getField("effective_date"))
      endDate = self.__ToDateTime(claim.getField("end_date"))

      doingBusinessAs = DoingBusinessAs.objects.filter(verifiableOrgId=verifiableOrg, dbaName=dbaName)
      if not doingBusinessAs:
        self.__logger.debug("DoingBusinessAs, {0}, does not exist.  Creating ...".format(dbaName))
        doingBusinessAs = DoingBusinessAs(
          verifiableOrgId = verifiableOrg,
          dbaName = dbaName,
          effectiveDate = effectiveDate,
          endDate = endDate
        )
        doingBusinessAs.save()
      else:
        self.__logger.debug("DoingBusinessAs, {0}, exists.  Updating ...".format(dbaName))
        doingBusinessAs = doingBusinessAs[0]
        doingBusinessAs.dbaName = dbaName
        doingBusinessAs.effectiveDate = effectiveDate
        doingBusinessAs.endDate = endDate
        doingBusinessAs.save()

      return doingBusinessAs

    def __CreateOrUpdateVerifiableClaim(self, claim: ClaimParser, verifiableClaimType: VerifiableClaimType, verifiableOrg: VerifiableOrg):      
      self.__logger.debug("Creating or updating the verifiable claim ...")
      
      # We don't have enough information to update an existing claim.
      verifiableClaim = VerifiableClaim.objects.filter(claimJSON=claim.json)
      effectiveDate = self.__ToDateTime(claim.getField("effective_date"))
      endDate = self.__ToDateTime(claim.getField("end_date"))
      
      if not verifiableClaim:
        self.__logger.debug("The verifiable claim does not exist.  Creating ...")
        verifiableClaim = VerifiableClaim(
          verifiableOrgId = verifiableOrg,
          claimType = verifiableClaimType,
          # Sould the claim be base64 encoded? i.e. claimJSON = base64.b64encode(claim.json)
          claimJSON = claim.json,
          effectiveDate = effectiveDate,
          endDate = endDate,
          inactiveClaimReasonId = None,
        )
        verifiableClaim.save()
      else:
        self.__logger.debug("The VerifiableClaim already exists ...")
        verifiableClaim = verifiableClaim[0]
      
      return verifiableClaim

    def __CreateOrUpdateLocation(self, claim: ClaimParser, verifiableOrg: VerifiableOrg, doingBusinessAs: DoingBusinessAs, locationTypeName: str):
      locationType = self.__get_LocationType(locationTypeName)
      addressee = claim.getField("addressee")
      addlDeliveryInfo = "{0}\r\n{1}".format(claim.getField("address_line_2"), claim.getField("country"))
      #unitNumber = claim.getField("")
      streetAddress = claim.getField("address_line_1")
      municipality = claim.getField("city")
      province = claim.getField("province")
      postalCode = claim.getField("postal_code")
      #latLong = claim.getField("")
      effectiveDate = self.__ToDateTime(claim.getField("effective_date"))
      endDate = self.__ToDateTime(claim.getField("end_date"))

      orgName = verifiableOrg.legalName
      if doingBusinessAs:
        orgName = doingBusinessAs.dbaName

      location = Location.objects.filter(verifiableOrgId=verifiableOrg, postalCode=postalCode)
      if not location:
        self.__logger.debug("Registering new location for {0} ...".format(orgName))
        location = Location(
          verifiableOrgId = verifiableOrg,
          doingBusinessAsId = doingBusinessAs,
          locationTypeId = locationType,
          addressee = addressee,
          addlDeliveryInfo = addlDeliveryInfo,
          #unitNumber = unitNumber,
          streetAddress = streetAddress,
          municipality = municipality,
          province = province,
          postalCode = postalCode,
          #latLong = latLong,
          effectiveDate = effectiveDate,
          endDate = endDate
        )
        location.save()
      else:
        self.__logger.debug("Updating location for {0} ... ".format(orgName))
        location = location[0]
        location.verifiableOrgId = verifiableOrg
        location.doingBusinessAsId = doingBusinessAs
        location.locationTypeId = locationType
        location.addressee = addressee
        location.addlDeliveryInfo = addlDeliveryInfo
        #location.unitNumber = unitNumber
        location.streetAddress = streetAddress
        location.municipality = municipality
        location.province = province
        location.postalCode = postalCode
        #location.latLong = latLong
        location.effectiveDate = effectiveDate
        location.endDate = endDate
        location.save()

      return location

    async def __StoreClaim(self, claim):
      self.__logger.debug("Storing the claim in the wallet ...")
      await self.__orgbook.store_claim(claim)
    
    def SaveClaim(self, claimJson):      
      claim = ClaimParser(claimJson)
      self.__logger.debug("Processing {0} claim ...".format(claim.claimType))

      # If the claim type has not been registered, reject the claim.
      verifiableClaimType = self.__get_VerifiableClaimType(claim)
      if not verifiableClaimType:
        raise ClaimTypeNotRegisteredException()

      # Look up the organization ...
      verifiableOrg = self.__get_VerifiableOrg(claim)

      # ToDo:
      # - Don't hard code the claim types at this level.  Get things working and refactor.
      # - Create claim processors that know how to deal with given claims.
      if claim.claimType == "incorporation.bc_registries":
        verifiableOrg = self.__CreateOrUpdateVerifiableOrg(claim, verifiableOrg)
        location = self.__CreateOrUpdateLocation(claim, verifiableOrg, None, "Headquarters")

      # All claims following the initial 'incorporation.bc_registries' claim MUST have an legal_entity_id (or'corp_num') field to relate the claim to the business.
      # If a mathcing VerifiableOrg record does not exist at this point, reject the claim.
      if not verifiableOrg:
        raise OrganizationNotRegisteredException()

      # Process the claim and store it in the wallet ...
      self.__CreateOrUpdateVerifiableClaim(claim, verifiableClaimType, verifiableOrg)
      eventloop.do(self.__StoreClaim(claim.json))

      # Process all other parsable claim types ...
      if claim.claimType == "doing_business_as.bc_registries":
        doingBusinessAs = self.__CreateOrUpdateDoingBusinessAs(claim, verifiableOrg)
        location = self.__CreateOrUpdateLocation(claim, verifiableOrg, doingBusinessAs, "Location")