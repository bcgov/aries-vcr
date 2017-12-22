from api.indy.claimParser import ClaimParser
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


# ToDo:
# * The code is currently making assumtions in order to fill in gaps in the infomration provided with a claim.
# ** VerifiableOrgType
# *** Taking the code from the claim, but where would we get a proper description?
# ** Jurisdiction
# *** Taking the name from the claim, but where would we get a proper abbrvation?
# ** IssuerService
# *** The claim provided the DID for the issue service, but where would we get the remainder of the infomration?
# *** The associated methods are hard coded the use the BC Registry.
# ** VerifiableClaimType
# *** How do we determine the claim type?
# *** Where would we get the infomration needed to fill in the record?
# *** The associated methods are hard coded the expect a 'Verified Organization' claim.
# *** Contains issuerURL which is duplicated in VerifiableClaimType.IssuerService.issuerOrgURL
# ** VerifiableClaim
# *** We don't have enough information to update an existing claim.
# *** Looking up the calim via the ClaimJSON is a bit cumbersome.  We should add a hash field that allows for more streamlined queries.
#     Is there something in the signature that we could use, such as the m2 field?

class ClaimProcesser(object):
    """
    Parses and processes a claim.

    _Currently only supports 'Verified Organization' claims._
    """

    def __init__(self) -> None:
      self.__orgbook = Agent()
      self.__logger = logging.getLogger(__name__)

    def __get_VerifiableOrgType(self, claim):
      orgTypeCode = claim["orgTypeId"]
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

    def __get_Jurisdiction(self, claim):
      jurisdictionName = claim["jurisdictionId"]
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

    def __CreateOrUpdateVerifiableOrg(self, claim):
      organizationId = claim["busId"]
      name = claim["LegalName"]

      verifiableOrg = VerifiableOrg.objects.filter(orgId=organizationId)
      if not verifiableOrg:
        self.__logger.debug("Organization, {0}, with business id {1} does not exist.  Creating ... ".format(name, organizationId))
        verifiableOrg = VerifiableOrg(
          orgId = claim["busId"],
          orgTypeId = self.__get_VerifiableOrgType(claim),
          jurisdictionId = self.__get_Jurisdiction(claim),
          legalName = claim["LegalName"],
          effectiveDate = claim["effectiveDate"]
        )
        verifiableOrg.save()
      else:
        self.__logger.debug("Organization, {0}, with business id {1} exists.  Updating ... ".format(name, organizationId))
        verifiableOrg = verifiableOrg[0]
        verifiableOrg.orgId = claim["busId"]
        verifiableOrg.orgTypeId = self.__get_VerifiableOrgType(claim)
        verifiableOrg.jurisdictionId = self.__get_Jurisdiction(claim)
        verifiableOrg.legalName = claim["LegalName"]
        verifiableOrg.effectiveDate = claim["effectiveDate"]
        verifiableOrg.save()

      return verifiableOrg

    def __get_IssuerService(self, claimParser):
      # We only have one issuer for the moment; the BC Registry
      issuerServiceDID = claimParser.issuer_did
      issuerServiceName = "BC Registry"
      issuerOrgTLA = "BCReg"
      issuerOrgURL = "https://bcregistries.gov.bc.ca"

      issuerService = IssuerService.objects.filter(DID=issuerServiceDID)
      if not issuerService:
        self.__logger.debug("IssuerService, {0}, does not exist.  Creating ...".format(issuerServiceDID))
        issuerService = IssuerService(
          name = issuerServiceName,
          issuerOrgTLA = issuerOrgTLA,
          issuerOrgURL = issuerOrgURL,
          DID = issuerServiceDID,
          jurisdictionId = self.__get_Jurisdiction(claimParser.claim),
          # effectiveDate = timezone.now,
          # endDate = None
        )
        issuerService.save()     
      else:
        self.__logger.debug("IssuerService, {0}, exists ...".format(issuerServiceDID))
        issuerService = issuerService[0]
      
      return issuerService

    def __get_VerifiableClaimType(self, claimParser):
      # We only have one claim type for the moment; a Verified Organization Claim Type
      base64Logo = None
      issuerURL = "https://registries.bc.gov.ca/verifiedOrganization"
      verifiableClaimTypeName = "Verified Organization"
      verifiableClaimType = VerifiableClaimType.objects.filter(claimType=verifiableClaimTypeName)
      
      # ToDo:
      # - Update or lookup this information
      schemaName = None
      schemaVersion = None

      if not verifiableClaimType:
        self.__logger.debug("VerifiableClaimType, {0}, does not exist.  Creating ...".format(verifiableClaimTypeName))
        verifiableClaimType = VerifiableClaimType(
          claimType = verifiableClaimTypeName,
          base64Logo = base64Logo,
          issuerServiceId = self.__get_IssuerService(claimParser),
          issuerURL = issuerURL,
          schemaName = schemaName,
          schemaVersion = schemaVersion,
          # effectiveDate = timezone.now,
          # endDate = None
        )
        verifiableClaimType.save()     
      else:
        self.__logger.debug("VerifiableClaimType, {0}, exists ...".format(verifiableClaimTypeName))
        verifiableClaimType = verifiableClaimType[0]
      
      return verifiableClaimType

    def __CreateOrUpdateVerifiableClaim(self, claimParser, verifiableOrg):      
      # We don't have enough information to update an existing claim.
      claim = claimParser.fullClaim
      verifiableClaim = VerifiableClaim.objects.filter(claimJSON=claim)
      if not verifiableClaim:
        self.__logger.debug("The VerifiableClaim does not exist.  Creating ...")
        verifiableClaim = VerifiableClaim(
          verifiableOrgId = verifiableOrg,
          claimType = self.__get_VerifiableClaimType(claimParser),
          claimJSON = claim,
          # Sould the claim be base64 encoded?
          # claimJSON = base64.b64encode(claimParser.claim),
          # effectiveDate = timezone.now,
          # endDate = None,
          inactiveClaimReasonId = None
        )
        verifiableClaim.save()
      else:
        self.__logger.debug("The VerifiableClaim exists ...")
      
      return verifiableClaim

    async def __StoreClaim(self, claim):
      await self.__orgbook.store_claim(claim)
    
    def SaveClaim(self, claimJson):      
      self.__logger.debug("Parsing claim ...")
      claimParser = ClaimParser(claimJson)      

      self.__logger.debug("Creating or updating the associated Verifiable Organization ...")
      verifiableOrg = self.__CreateOrUpdateVerifiableOrg(claimParser.claim)

      self.__logger.debug("Creating or updating the associated Verifiable Claim ...")
      self.__CreateOrUpdateVerifiableClaim(claimParser, verifiableOrg)

      self.__logger.debug("Storing the claim in the wallet ...")
      eventloop.do(self.__StoreClaim(claimParser.rawClaim))