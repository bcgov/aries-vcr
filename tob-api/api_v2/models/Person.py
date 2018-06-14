from django.db import models
from django.utils import timezone

from auditable.models import Auditable

from .Credential import Credential


class Person(Auditable):
    credentials = models.ManyToManyField(Credential, related_name="people")
    full_name = models.TextField(null=True)
    type = models.TextField(null=True)

    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = "person"
