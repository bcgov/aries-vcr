"""
    REST API Documentation for TheOrgBook

    TheOrgBook is a repository for Verifiable Claims made about Organizations related to a known foundational Verifiable Claim. See https://github.com/bcgov/VON

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

import datetime

from django.db import models
from django.utils import timezone
from .UserRole import UserRole

class CurrentUserViewModel(models.Model):	    
    givenName = models.CharField(max_length=255, blank=True, null=True)   
    surname = models.CharField(max_length=255, blank=True, null=True)   
    email = models.CharField(max_length=255, blank=True, null=True)   
    active = models.BooleanField()   
    userRoles = models.ManyToManyField('UserRole', related_name='CurrentUserViewModeluserRoles', blank=True)   
    smUserId = models.CharField(max_length=255, blank=True, null=True)   
    smAuthorizationDirectory = models.CharField(max_length=255, blank=True, null=True)   
    class Meta:
      abstract = True
