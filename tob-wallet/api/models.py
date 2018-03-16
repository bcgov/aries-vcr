from django.db import models
# the following 4 imports are for DRF tokens only, comment out for JWT tokens
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


# The following method is for DRF tokens only, comment out for JWT tokens
# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class WalletItem(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    wallet_name = models.CharField(max_length=255, blank=False)
    item_type = models.CharField(max_length=255, blank=False)
    item_id = models.CharField(max_length=255, blank=False)
    item_value = models.TextField(blank=False)
    created_by = models.ForeignKey('auth.User', related_name='wallet_items', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('wallet_name', 'item_type', 'item_id',)
