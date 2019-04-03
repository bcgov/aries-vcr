from .models.Subscription import Subscription
from .models.CredentialHook import CredentialHook


def find_and_fire_hook(event_name, instance, **kwargs):
    filters = {
        'event': event_name,
        'is_active': True,
    }

    hooks = CredentialHook.objects.filter(**filters)
    for hook in hooks:
        # TODO find subscription(s) related to this hook
        print("hook", hook)
        subscriptions = Subscription.objects.filter(hook=hook).all()
        if 0 < len(subscriptions):
            # TODO check if we should fire per subscription
            for subscription in subscriptions:
                print("subscription", subscription)

        hook.deliver_hook(instance)

