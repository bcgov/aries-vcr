from api.indy.claimParser import ClaimParser
from api.models.Jurisdiction import Jurisdiction
from api.models.VerifiableOrgType import VerifiableOrgType
from api.models.VerifiableOrg import VerifiableOrg

class ClaimProcesser(object):
    """
    description of class
    """

    def __get_VerifiableOrgType(self, claim):
      orgTypeCode = claim["orgTypeId"]
      verifiableOrgType = VerifiableOrgType.objects.filter(orgType=orgTypeCode)
      if not verifiableOrgType:
        verifiableOrgType = VerifiableOrgType(
          orgType = orgTypeCode,
          description = orgTypeCode,
          displayOrder = 0          
        )
        verifiableOrgType.save()
      else:
        verifiableOrgType = verifiableOrgType[0]
      
      return verifiableOrgType

    def __get_Jurisdiction(self, claim):
      jurisdictionName = claim["jurisdictionId"]
      jurisdiction = Jurisdiction.objects.filter(name=jurisdictionName)
      if not jurisdiction:
        jurisdiction = Jurisdiction(
          abbrv = jurisdictionName,
          name = jurisdictionName,
          displayOrder = 0,
          isOnCommonList = True
        )
        jurisdiction.save()
      else:
        jurisdiction = jurisdiction[0]
      
      return jurisdiction

    def __VerifiableOrgExists(self, claim):
      verifiableOrgExists = False
      organizationId = claim["busId"]
      verifiableOrg = VerifiableOrg.objects.filter(orgId=organizationId)
      if verifiableOrg:
        verifiableOrgExists = True

      return verifiableOrgExists
    
    def SaveClaim(self, claimJson):
      claimParser = ClaimParser(claimJson)
      claim = claimParser.claim

      if not self.__VerifiableOrgExists(claim):
        verifiableOrg = VerifiableOrg(
          orgId = claim["busId"],
          orgTypeId = self.__get_VerifiableOrgType(claim),
          jurisdictionId = self.__get_Jurisdiction(claim),
          legalName = claim["LegalName"],
          effectiveDate = claim["effectiveDate"]
        )
        verifiableOrg.save()

      # ToDo:
      # * Save the claim.
      # ** Requires a claim type be created first.


