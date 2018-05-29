from django.db import models
from django.utils import timezone

from auditable.models import Auditable


class Schema(Auditable):
    name = models.TextField()
    version = models.TextField()
    publisher_did = models.TextField()

    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = "schema"
