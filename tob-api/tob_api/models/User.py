from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    DID = models.TextField(max_length=60, blank=True, unique=True)
    verkey = models.BinaryField(blank=True)
    display_name = models.TextField(blank=True)

    class Meta:
        db_table = 'api_user'