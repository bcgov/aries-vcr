import django.db.models.deletion
from django.contrib.auth import get_user_model
from django.db import models

from api_v2.models.Auditable import Auditable


class HookUser(Auditable):
    user = models.ForeignKey(
        get_user_model(), 
        related_name="hook_user",
        on_delete=django.db.models.deletion.CASCADE
    )

    # the following are for web hook registration
    # userid = re-used generated for web hooks subscribers
    # password = re-used generated registration token
    email = models.TextField(max_length=240)
    # generated by us; subscriber needs to confirm every 3 months (at least call PUT to update registration)
    registration_expiry = models.DateField(blank=True, null=True)
    # org_name provided by subscriber
    org_name = models.TextField(max_length=240)
    # url to call (optional - can be provided per subscription)
    target_url = models.TextField(max_length=240, blank=True, null=True)
    # token to provide with hook calls (optional - can be provided per subscription)
    hook_token = models.TextField(max_length=240, blank=True, null=True)
