"""
    REST API Documentation for TheOrgBook

    TheOrgBook is a repository for Verified Claims made about Organizations related to a known foundational Verified Claim. See https://github.com/bcgov/VON

    OpenAPI spec version: v1
        

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from django.contrib import admin

from .models.InactiveClaimReason import InactiveClaimReason
from .models.IssuerService import IssuerService
from .models.Jurisdiction import Jurisdiction
from .models.Permission import Permission

from .models.Role import Role
from .models.RolePermission import RolePermission


from .models.User import User

from .models.UserRole import UserRole


from .models.VOClaim import VOClaim
from .models.VOClaimType import VOClaimType
from .models.VODoingBusinessAs import VODoingBusinessAs
from .models.VOLocation import VOLocation
from .models.VOLocationType import VOLocationType
from .models.VOType import VOType
from .models.VerifiedOrg import VerifiedOrg



admin.site.register(InactiveClaimReason)
admin.site.register(IssuerService)
admin.site.register(Jurisdiction)
admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(RolePermission)
admin.site.register(User)
admin.site.register(UserRole)
admin.site.register(VOClaim)
admin.site.register(VOClaimType)
admin.site.register(VODoingBusinessAs)
admin.site.register(VOLocation)
admin.site.register(VOLocationType)
admin.site.register(VOType)
admin.site.register(VerifiedOrg)