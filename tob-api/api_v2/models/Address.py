from django.db import models
from django.utils import timezone

from auditable.models import Auditable

from .Credential import Credential


class Address(Auditable):
    credential = models.ManyToManyField(Credential, related_name="addresses")
    addressee = models.TextField()
    civic_address = models.TextField()
    city = models.TextField()
    province = models.TextField()
    country = models.TextField()
    address_type = models.TextField()

    postal_code = models.TextField()
    country_code = models.TextField()

    latitude = models.TextField(null=True)
    longitude = models.TextField(null=True)

    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = "address"
        unique_together = (("postal_code", "country_code"),)
