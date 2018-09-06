from django.db import models

from auditable.models import Auditable

from .Credential import Credential


class Category(Auditable):
    reindex_related = ['credential']

    credential = models.ForeignKey(Credential, related_name="categories", on_delete=models.CASCADE)
    type = models.TextField(null=True)
    value = models.TextField(null=True)

    class Meta:
        db_table = "category"
