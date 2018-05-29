from django.db import models
from django.utils import timezone

from auditable.models import Auditable

from .Credential import Credential


class Name(Auditable):
    credential = models.ManyToManyField(Credential, related_name="names")
    text = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)

    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
