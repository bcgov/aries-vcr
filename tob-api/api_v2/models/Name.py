from django.db import models
from django.utils import timezone

from auditable.models import Auditable

from .Credential import Credential


class Name(Auditable):
    credential = models.ManyToManyField(Credential, related_name="names")
    text = models.TextField()
    type = models.TextField()
    language = models.TextField()

    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = "name"
        unique_together = (("text", "type", "language"),)
