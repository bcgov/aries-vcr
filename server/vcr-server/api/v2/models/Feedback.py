from django.db import models
from django.utils import timezone
import datetime

class Feedback(models.Model):

    like = models.BooleanField(null=True)
    ip = models.GenericIPAddressField(null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "feedback"
        ordering = ("id",)
