from django.db import models
from django.utils import timezone

from auditable.models import Auditable

from .Credential import Credential


class Name(Auditable):
    credentials = models.ManyToManyField(Credential, related_name="names")
    text = models.TextField(null=True)
    type = models.TextField(null=True)
    language = models.TextField(null=True)
    source_id = models.TextField(null=True)
    is_legal = models.BooleanField(null=True)
    
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = "name"
