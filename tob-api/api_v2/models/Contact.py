from django.db import models

from auditable.models import Auditable

from .Credential import Credential


class Contact(Auditable):
    reindex_related = ['credential']
    
    credential = models.ForeignKey(Credential, related_name="contacts")
    text = models.TextField(null=True)
    type = models.TextField(null=True)

    class Meta:
        db_table = "contact"
