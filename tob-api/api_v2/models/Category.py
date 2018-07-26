from django.db import models

from auditable.models import Auditable

from .Credential import Credential


class Category(Auditable):
    credential = models.ForeignKey(Credential, related_name="categories")
    type = models.TextField(null=True)
    value = models.TextField(null=True)

    class Meta:
        db_table = "category"
