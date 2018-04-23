from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    DID = models.TextField(max_length=60, blank=True, unique=True)
    verkey = models.TextField(max_length=100, blank=True)

