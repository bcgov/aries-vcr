from django.db import models
from django.utils import timezone

from auditable.models import Auditable

from .Credential import Credential


class Address(Auditable):
    credentials = models.ManyToManyField(Credential, related_name="addresses")
    addressee = models.TextField(null=True)
    civic_address = models.TextField(null=True)
    city = models.TextField(null=True)
    province = models.TextField(null=True)
    postal_code = models.TextField(null=True)
    country = models.TextField(null=True)
    type = models.TextField(null=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = "address"
