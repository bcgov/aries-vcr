from django.db import models
from django.utils import timezone

from auditable.models import Auditable

from .Credential import Credential


class Claim(Auditable):
    credential = models.ForeignKey(Credential, related_name="claims")
    name = models.TextField(blank=True, null=True)
    value = models.TextField(blank=True, null=True)

    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
