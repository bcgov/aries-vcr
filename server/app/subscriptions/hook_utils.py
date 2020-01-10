import datetime
import time

from .models.CredentialHook import CredentialHook
from .models.HookUser import HookUser
from .models.Subscription import Subscription

from api_v2.utils import log_timing_method


def find_and_fire_hook(event_name, instance, **kwargs):
    filters = {"event": event_name, "is_active": True}

    start_time = time.perf_counter()
    method = "web_hook." + event_name
    hooks = CredentialHook.objects.filter(**filters)
    for hook in hooks:
        if is_registration_valid(hook):
            send_hook = False
            # find subscription(s) related to this hook
            subscriptions = Subscription.objects.filter(hook=hook).all()
            if 0 < len(subscriptions):
                # check if we should fire per subscription
                for subscription in subscriptions:
                    if subscription.subscription_expiry is not None:
                        # skip for any non-null subscription expiry date
                        pass
                    elif subscription.subscription_type == "New":
                        if subscription.subscription_type == instance.topic_status:
                            send_hook = True
                    elif subscription.subscription_type == "Stream":
                        if (
                            subscription.topic_source_id == instance.corp_num
                            and subscription.credential_type == instance.credential_type
                        ):
                            send_hook = True
                    elif subscription.subscription_type == "Topic":
                        if subscription.topic_source_id == instance.corp_num:
                            send_hook = True
                    else:
                        print(
                            "      >>> Error invalid subscription type:",
                            subscription.subscription_type,
                        )
                        raise Exception("Invalid subscription type")

            # logic around whether we hook or not
            if send_hook:
                hook_start_time = time.perf_counter()
                hook_method = "web_hook.deliver_hook"

                hook.deliver_hook(instance)
                
                hook_end_time = time.perf_counter()
                log_timing_method(hook_method, hook_start_time, hook_end_time, True)

    end_time = time.perf_counter()
    log_timing_method(method, start_time, end_time, True)


def is_registration_valid(hook: CredentialHook):
    is_valid = True
    hook_user = HookUser.objects.get(user__id=hook.user_id)

    if hook_user.registration_expiry < datetime.datetime.now().date():
        is_valid = False
        deactivate_hook(hook.id)

    return is_valid


def deactivate_hook(hook_id: int):
    cred_hook = CredentialHook.objects.get(id=hook_id)
    cred_hook.is_active = False
    cred_hook.save()
