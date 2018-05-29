from django.db import models
from django.utils import timezone

from auditable.models import Auditable


class Issuer(Auditable):
    did = models.TextField()
    name = models.TextField()
    abbreviation = models.TextField()
    email = models.TextField()
    url = models.TextField()

    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = "issuer"
