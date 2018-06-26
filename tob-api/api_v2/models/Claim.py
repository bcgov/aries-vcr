from django.db import models

from auditable.models import Auditable

from .Credential import Credential


class Claim(Auditable):
    credential = models.ForeignKey(Credential, related_name="claims")
    name = models.TextField(blank=True, null=True)
    value = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "claim"
