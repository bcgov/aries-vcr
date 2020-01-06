import threading

from enum import Enum

timing_lock = threading.Lock()
timings = {}


class HookStep(Enum):
    FIRST_ATTEMPT = "first_attempt"
    RETRY = "retry_attempt"
    RETRY_FAIL = "retry_fail"


class TooManyRetriesException(Exception):
    pass


def log_webhook_execution_result(method, success, hook_step=None, data=None):
    global timings

    timing_lock.acquire()
    try:
        if method not in timings:
            timings[method] = {
                "total_count": 1,
                "success_count": 1 if success else 0,
                "fail_count": 0 if success else 1,
                "retry_count": 1 if hook_step == HookStep.RETRY else 0,
                "retry_fail_count": 1 if hook_step == HookStep.RETRY_FAIL else 0,
                "data": {},
            }
        else:
            timings[method]["total_count"] = timings[method]["total_count"] + 1
            if success:
                timings[method]["success_count"] = timings[method]["success_count"] + 1
            else:
                timings[method]["fail_count"] = timings[method]["fail_count"] + 1
            if hook_step == HookStep.RETRY:
                timings[method]["retry_count"] = timings[method]["fail_count"] + 1
            if hook_step == HookStep.RETRY_FAIL:
                timings[method]["retry_fail_count"] = timings[method]["fail_count"] + 1
        if data:
            timings[method]["data"][str(timings[method]["total_count"])] = data
    finally:
        timing_lock.release()
