from django.db import models

from auditable.models import Auditable


class Issuer(Auditable):
    did = models.TextField(unique=True)
    name = models.TextField()
    abbreviation = models.TextField()
    email = models.TextField()
    url = models.TextField()

    class Meta:
        db_table = "issuer"
