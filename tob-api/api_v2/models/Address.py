from django.db import models
from django.utils import timezone

from auditable.models import Auditable

from .Credential import Credential


class Address(Auditable):
    credential = models.ManyToManyField(Credential, related_name="addresses")
    addressee = models.TextField(blank=True, null=True)
    civic_address = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    province = models.TextField(blank=True, null=True)
    postal_code = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    address_type = models.TextField(blank=True, null=True)

    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = "address"
