"""
    REST API Documentation for TheOrgBook

    TheOrgBook is a repository for Verifiable Claims made about Organizations related to a known foundational Verifiable Claim. See https://github.com/bcgov/VON

    OpenAPI spec version: v2
        

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

import datetime

from django.db import models
from django.utils import timezone

from auditable.models import Auditable


class Address(Auditable):
    credential = models.ManyToManyField('Credential', related_name='addresses')
    addressee = models.TextField(blank=True, null=True)
    civicAddress = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    province = models.TextField(blank=True, null=True)
    postalCode = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    addressType = models.TextField(blank=True, null=True)

    startDate = models.DateField(default=timezone.now)
    endDate = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'ADDRESS'
