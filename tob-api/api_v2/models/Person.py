from django.db import models

from auditable.models import Auditable

from .Credential import Credential


class Person(Auditable):
    credential = models.ForeignKey(Credential, related_name="people")
    full_name = models.TextField(null=True)

    class Meta:
        db_table = "person"
