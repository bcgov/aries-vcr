import logging
import os
import threading
from enum import Enum

from .models.CredentialHookStats import CredentialHookStats

LOGGER = logging.getLogger(__name__)


class HookStep(Enum):
    FIRST_ATTEMPT = "first_attempt"
    RETRY = "retry_attempt"
    RETRY_FAIL = "retry_fail"


class TooManyRetriesException(Exception):
    pass


def log_webhook_execution_result(success, hook_step=None, json_data=None):

    worker_name = os.environ["CELERY_WORKER_NAME"]
    if worker_name is None:
        LOGGER.warning(
            "No name set for current worker, falling back to using OS-assigned thread ID"
        )
        worker_name = threading.get_native_id()

    # Store stats for current worker
    current_stats = (
        CredentialHookStats.objects.filter(worker_id=worker_name).first()
        or CredentialHookStats(worker_id=worker_name)
    )

    if success is False or hook_step is HookStep.FIRST_ATTEMPT:
        current_stats.attempt_count = current_stats.attempt_count + 1
        current_stats.total_count = current_stats.total_count + 1
    elif success is False and hook_step is HookStep.RETRY:
        current_stats.retry_count = current_stats.retry_count + 1
        current_stats.total_count = current_stats.total_count + 1
    elif success is False and hook_step is HookStep.RETRY_FAIL:
        current_stats.retry_fail_count = current_stats.retry_fail_count + 1
    elif success is False and hook_step is None:
        current_stats.fail_count = current_stats.fail_count + 1
    elif success is True:
        current_stats.success_count = current_stats.success_count + 1
    else:
        LOGGER.warning(
            f"Unexpected argument combination: success={success}, hook_step={hook_step}"
        )

    current_stats.save()
