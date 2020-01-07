import json
import logging
import os
from datetime import datetime

import pytz
import requests
from celery.exceptions import Retry
# from celery.result import AsyncResult
from celery.signals import celeryd_after_setup
from celery.task import Task
from django.conf import settings

from icat_hooks.models.Subscription import Subscription

from .utils import HookStep, TooManyRetriesException, log_webhook_execution_result

LOGGER = logging.getLogger(__name__)


# class DeliverHookError(Task):
#     def run(self, uuid):
#         # uuid = self.request.id
#         print("Task", uuid)
#         # result = AsyncResult(uuid)
#         # exc = result.get(propagate=False)
#         # LOGGER.error(
#         #     "Task {0} raised exception: {1!r}\n{2!r}".format(
#         #         uuid, exc, result.traceback
#         #     )
#         # )


class DeliverHook(Task):
    max_retries = 5

    def run(self, target, payload, instance_id=None, hook_id=None, **kwargs):
        """
        target:     the url to receive the payload.
        payload:    a python primitive data structure
        instance_id:   a possibly None "trigger" instance ID
        hook_id:       the ID of defining Hook object
        """

        try:
            try:
                # raise this exception here to test error handling
                # raise Exception("Fake Error!!!!!")

                log_webhook_execution_result(False, HookStep.FIRST_ATTEMPT)

                LOGGER.info("Delivering hook to: {}".format(target))
                response = requests.post(
                    url=target,
                    data=json.dumps(payload),
                    headers={"Content-Type": "application/json"},
                )
                LOGGER.info("--> response {}".format(response.status_code))
                response.raise_for_status()

                # find subscription and set last successful sent date, and set error count to zero
                subscription = Subscription.objects.get(
                    pk=payload["subscription"]["id"]
                )
                subscription.last_sent_date = datetime.now(pytz.utc)
                subscription.error_count = 0
                subscription.save()

                log_webhook_execution_result(True)

            except requests.exceptions.HTTPError as e:
                if self.request.retries < settings.HOOK_RETRY_THRESHOLD:
                    delay_in_seconds = settings.HOOK_RETRY_DELAY ** self.request.retries
                    log_webhook_execution_result(False, HookStep.RETRY)
                    self.retry(countdown=delay_in_seconds)
                else:
                    # let the error propagate
                    LOGGER.debug("Too many retries, propagate error")
                    log_webhook_execution_result(False, HookStep.RETRY_FAIL)
                    raise TooManyRetriesException(e)
        except Retry as e:
            # ignore this one
            LOGGER.debug("Ignore Retry exception")
            pass
        except Exception as e:
            # update error status of subscription
            try:
                """ Example payload:
                {
                  'subscription':
                    {'id': 2, 'owner': 'anon-ybgshtl14hjp2n6s7xcl0s99ztkosd2o', 'subscription_type': 'New', 'topic_id': 'BC0123456', 'credential_type': None, 'target_url': 'http://ip10-0-172-4-bnpd0ndm4dlga5djnpn0-8000.direct.play-with-von.vonx.io/api/echo', 'hook_token': 'ashdkjahsdkjhaasd88a7d9a8sd9asasda'}, 
                  'data': 
                    {'id': 2198, 'corp_num': 'BC1093807', 'credential_type': 'registration.registries.ca', 
                      'credential_json': {'cred_def_id': '6qnvgJtqwK44D8LFYnV5Yf:3:CL:10:default', 'schema_name': 'registration.registries.ca', 
                        'attributes': {'expiry_date': '', 'registration_expiry_date': '', 'registration_renewal_effective': '', 'entity_status_effective': '2019-12-13T00:42:53+00:00', 'effective_date': '2019-12-13T00:42:53+00:00', 'entity_name_trans': '', 'registration_date': '2016-10-20T21:55:46+00:00', 'entity_name_effective': '2019-12-13T00:42:53+00:00', 'home_jurisdiction': 'BC', 'entity_name': '1093807 B.C. LTD.', 'reason_description': 'Filing:RESTF', 'registration_id': 'BC1093807', 'entity_type': 'BC', 'entity_name_trans_effective': '', 'extra_jurisdictional_registration': '', 'entity_status': 'ACT', 'entity_name_assumed': '', 'entity_name_assumed_effective': '', 'registered_jurisdiction': ''}
                      }
                    }
                }
                """
                LOGGER.debug("Error sending hook to:", payload["subscription"])
                LOGGER.debug(
                    "Credential Type:",
                    payload["data"]["credential_json"]["schema_name"],
                )
                LOGGER.debug(
                    "Credential:", payload["data"]["credential_json"]["attributes"]
                )

                # TODO - update subscription last error date, increment error count, and potentially update status
                subscription = Subscription.objects.get(
                    pk=payload["subscription"]["id"]
                )
                subscription.last_error_date = datetime.now(pytz.utc)
                subscription.error_count = subscription.error_count + 1
                # if too many consecutive errors expire the subscription
                if subscription.error_count > settings.HOOK_MAX_SUBSCRIPTION_ERRORS:
                    subscription.subscription_expiry = datetime.now()
                subscription.save()

                log_webhook_execution_result(False)

            except Exception as e2:
                LOGGER.error("Failed to update subscription error status", e2)
                pass
            raise e


def deliver_hook_wrapper(target, payload, instance, hook):
    # instance is None if using custom event, not built-in
    if instance is not None:
        instance_id = instance.id
    else:
        instance_id = None
    # pass ID's not objects because using pickle for objects is a bad thing
    kwargs = dict(
        target=target, payload=payload, instance_id=instance_id, hook_id=hook.id
    )
    # deliver_hook_error = DeliverHookError()
    # result = DeliverHook.apply_async(kwargs=kwargs, link_error=deliver_hook_error.s())
    result = DeliverHook.apply_async(kwargs=kwargs)
    result.forget()


@celeryd_after_setup.connect
def capture_worker_name(sender, instance, **kwargs):
    """
    Retrieves the current worker name (it can be set when starting the worker with the -n flag)
    and stores it in the app configuration.
    """
    if "CELERY_WORKER_NAME" not in os.environ:
        os.environ["CELERY_WORKER_NAME"] = "{0}".format(sender)
        LOGGER.info(f'Setting worker name: {os.environ["CELERY_WORKER_NAME"]}')
