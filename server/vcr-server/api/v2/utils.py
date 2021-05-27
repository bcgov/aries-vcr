"""
A collection of utility classes for TOB
"""

import logging
import os
import threading
from datetime import datetime, timedelta
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time
import json


from subscriptions.models import CredentialHookStats

from django.conf import settings
from django.forms.models import model_to_dict
from django.db import connection
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from haystack.query import SearchQuerySet
from pysolr import SolrError
from rest_framework import permissions
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

LOGGER = logging.getLogger(__name__)
DT_FMT = '%Y-%m-%d %H:%M:%S.%f%z'

# need to specify an env variable RECORD_TIMINGS=True to get method timings
RECORD_TIMINGS = os.getenv("RECORD_TIMINGS", "True").lower() == "true"
TRACE_EVENTS = os.getenv("TRACE_EVENTS", "True").lower() == "true"
TRACE_LABEL = os.getenv("TRACE_LABEL", "avcr.controller")
TRACE_TAG = os.getenv("TRACE_TAG", "acapy.events")
TRACE_LOG_TARGET = "log"
TRACE_TARGET = os.getenv("TRACE_TARGET", TRACE_LOG_TARGET)

timing_lock = threading.Lock()
timings = {}


def fetch_custom_settings(*args):
    _values = {}

    if not hasattr(settings, "CUSTOMIZATIONS"):
        return _values

    _dict = settings.CUSTOMIZATIONS
    for arg in args:
        if not _dict[arg]:
            return _values
        _dict = _dict[arg]

    return _dict


def apply_custom_methods(cls, *args):
    functions = list(fetch_custom_settings(*args))
    for function in functions:
        setattr(cls, function.__name__, classmethod(function))


def model_counts(model_cls, cursor=None, optimize=None):
    if optimize is None:
        optimize = getattr(settings, "OPTIMIZE_TABLE_ROW_COUNTS", True)
    if not optimize:
        return model_cls.objects.count()
    close = False
    try:
        if not cursor:
            cursor = connection.cursor()
            close = True
        cursor.execute(
            "SELECT reltuples::BIGINT AS estimate FROM pg_class WHERE relname=%s",
            [model_cls._meta.db_table],
        )
        row = cursor.fetchone()
    finally:
        if close:
            cursor.close()
    return row[0]


def record_count(model_cls, cursor=None):
    close = False
    try:
        if not cursor:
            cursor = connection.cursor()
            close = True
        query = "SELECT count(*) FROM %s" % model_cls._meta.db_table
        cursor.execute(query)
        row = cursor.fetchone()
    finally:
        if close:
            cursor.close()
    return row[0]


def solr_counts():
    total_q = SearchQuerySet()
    latest_q = total_q.filter(latest=True)
    registrations_q = latest_q.filter(category="entity_status::ACT")
    last_24h = datetime.now() - timedelta(days=1)
    last_week = datetime.now() - timedelta(days=7)
    last_month = datetime.now() - timedelta(days=30)
    last_24h_q = total_q.filter(create_timestamp__gte=last_24h)
    last_week_q = total_q.filter(create_timestamp__gte=last_week)
    last_month_q = total_q.filter(create_timestamp__gte=last_month)
    try:
        return {
            "total_indexed_items": total_q.count(),
            "active": latest_q.count(),
            "registrations": registrations_q.count(),
            "last_month": last_month_q.count(),
            "last_week": last_week_q.count(),
            "last_24h": last_24h_q.count(),
        }
    except SolrError:
        LOGGER.exception("Error when retrieving quickload counts from Solr")
        return False


@swagger_auto_schema(
    method="get", operation_id="api_v2_status_reset", operation_description="quick load"
)
@api_view(["GET"])
@authentication_classes(())
@permission_classes((permissions.AllowAny,))
def clear_stats(request, *args, **kwargs):
    global timings
    timing_lock.acquire()
    try:
        timings = {}
        return JsonResponse({"success": True})
    finally:
        timing_lock.release()


@swagger_auto_schema(
    method="get", operation_id="api_v2_status", operation_description="quick load"
)
@api_view(["GET"])
@authentication_classes(())
@permission_classes((permissions.AllowAny,))
def get_stats(request, *args, **kwargs):
    global timings
    timing_lock.acquire()
    try:
        hook_worker_stats = {}
        if "subscriptions" in settings.INSTALLED_APPS:
            # Only add hook stats IF the module is enabled/in use
            for item in CredentialHookStats.objects.all():
                hook_worker_stats[f"web_hook.worker_stats.{item.worker_id}"] = {
                    "total_count": item.total_count,
                    "attempt_count": item.attempt_count,
                    "success_count": item.success_count,
                    "fail_count": item.fail_count,
                    "retry_count": item.retry_count,
                    "retry_fail_count": item.retry_fail_count
                }
        return JsonResponse({**timings, **hook_worker_stats})
    finally:
        timing_lock.release()


def log_timing_method(method, start_time, end_time, success, data=None):
    global timings

    if not RECORD_TIMINGS:
        return

    timing_lock.acquire()
    try:
        elapsed_time = end_time - start_time
        if method not in timings:
            timings[method] = {
                "total_count": 1,
                "success_count": 1 if success else 0,
                "fail_count": 0 if success else 1,
                "min_time": elapsed_time,
                "max_time": elapsed_time,
                "total_time": elapsed_time,
                "avg_time": elapsed_time,
                "data": {},
            }
        else:
            timings[method]["total_count"] = timings[method]["total_count"] + 1
            if success:
                timings[method]["success_count"] = timings[method]["success_count"] + 1
            else:
                timings[method]["fail_count"] = timings[method]["fail_count"] + 1
            if elapsed_time > timings[method]["max_time"]:
                timings[method]["max_time"] = elapsed_time
            if elapsed_time < timings[method]["min_time"]:
                timings[method]["min_time"] = elapsed_time
            timings[method]["total_time"] = timings[method]["total_time"] + elapsed_time
            timings[method]["avg_time"] = (
                timings[method]["total_time"] / timings[method]["total_count"]
            )
        if data:
            timings[method]["data"][str(timings[method]["total_count"])] = data
    finally:
        timing_lock.release()


def log_timing_event(method, message, start_time, end_time, success):
    """Record a timing event in the system log or http endpoint."""

    if (not TRACE_EVENTS) and (not message.get("trace")):
        return
    if not TRACE_TARGET:
        return

    msg_id = "N/A"
    thread_id = message["thread_id"] if message.get("thread_id") else "N/A"
    handler = TRACE_LABEL
    ep_time = time.time()
    str_time = datetime.utcfromtimestamp(ep_time).strftime(DT_FMT)
    if end_time:
        outcome = method + ".SUCCESS" if success else ".FAIL"
    else:
        outcome = method + ".START"
    event = {
        "msg_id": msg_id,
        "thread_id": thread_id if thread_id else msg_id,
        "traced_type": method,
        "timestamp": ep_time,
        "str_time": str_time,
        "handler": str(handler),
        "ellapsed_milli": int(1000 * (end_time - start_time)) if end_time else 0,
        "outcome": outcome,
    }
    event_str = json.dumps(event)

    try:
        if TRACE_TARGET == TRACE_LOG_TARGET:
            # write to standard log file
            LOGGER.setLevel(logging.INFO)
            LOGGER.info(" %s %s", TRACE_TAG, event_str)
        else:
            # should be an http endpoint
            _ = requests.post(
                TRACE_TARGET + TRACE_TAG,
                data=event_str,
                headers={"Content-Type": "application/json"}
            )
    except Exception as e:
        LOGGER.error(
            "Error logging trace target: %s tag: %s event: %s",
            TRACE_TARGET,
            TRACE_TAG,
            event_str
        )
        LOGGER.exception(e)


def call_agent_with_retry(agent_url, post_method=True, payload=None, headers=None, retry_count=5, retry_wait=1):
    """
    Post with retry - if returned status is 503 (or other select errors) unavailable retry a few times.
    """
    try:
        session = requests.Session()
        retry = Retry(
            total=retry_count,
            connect=retry_count,
            status=retry_count,
            status_forcelist=[
                429,  # too many requests
                500,  # Internal server error
                502,  # Bad gateway
                503,  # Service unavailable
                504   # Gateway timeout
            ],
            method_whitelist=['HEAD', 'TRACE', 'GET',
                              'POST', 'PUT', 'OPTIONS', 'DELETE'],
            read=0,
            redirect=0,
            backoff_factor=retry_wait
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        if post_method:
            resp = session.post(
                agent_url,
                json=payload,
                headers=headers,
            )
        else:
            resp = session.get(
                agent_url,
                headers=headers,
            )
        return resp
    except Exception as e:
        LOGGER.error("Agent connection raised exception, raise: " + str(e))
        raise


def local_name(names=[]):
    if len(names) == 0:
        return None
    try:
        types = [name.type for name in names]
        local_name = None
        # Order matters here
        for type in ['display_name', 'entity_name_assumed', 'entity_name']:
            if type in types:
                local_name = names[types.index(type)]
                break
        if not local_name:
            # Take the first one
            local_name = names[0]
        return local_name
    except Exception as e:
        LOGGER.error("Exception was raised: " + str(e))
        return None



def remote_name(names=[]):
    if len(names) == 0:
        return None
    try:
        types = [name.type for name in names]
        remote_name = None
        if 'entity_name_assumed' in types and 'entity_name' in types:
            remote_name = names[types.index('entity_name')]
        return remote_name
    except Exception as e:
        LOGGER.error("Exception was raised: " + str(e))
        return None

