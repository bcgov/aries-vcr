"""
A collection of utility classes for TOB
"""

import json
import os
import threading
import time

import logging
from datetime import datetime, timedelta

from django.conf import settings
from django.db import connection
from haystack.query import SearchQuerySet
from pysolr import SolrError

LOGGER = logging.getLogger(__name__)


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
            "total": total_q.count(),
            "active": latest_q.count(),
            "registrations": registrations_q.count(),
            "last_month": last_month_q.count(),
            "last_week": last_week_q.count(),
            "last_24h": last_24h_q.count(),
        }
    except SolrError:
        LOGGER.exception("Error when retrieving quickload counts from Solr")
        return False


from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import permissions
from django.http import JsonResponse

# need to specify an env variable RECORD_TIMINGS=True to get method timings
RECORD_TIMINGS = (os.getenv('RECORD_TIMINGS', 'True').lower() == 'true')

timing_lock = threading.Lock()
timings = {}

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
        return JsonResponse(timings)
    finally:
        timing_lock.release()

def log_timing_method(method, start_time, end_time, success, data=None):
    global timings

    if not RECORD_TIMINGS:
        return

    timing_lock.acquire()
    try:
        elapsed_time = end_time - start_time
        if not method in timings:
            timings[method] = {
                'total_count': 1,
                'success_count': 1 if success else 0,
                'fail_count': 0 if success else 1,
                'min_time': elapsed_time,
                'max_time': elapsed_time,
                'total_time': elapsed_time,
                'avg_time': elapsed_time,
                'data': {}
            }
        else:
            timings[method]['total_count'] = timings[method]['total_count'] + 1
            if success:
                timings[method]['success_count'] = timings[method]['success_count'] + 1
            else:
                timings[method]['fail_count'] = timings[method]['fail_count'] + 1
            if elapsed_time > timings[method]['max_time']:
                timings[method]['max_time'] = elapsed_time
            if elapsed_time < timings[method]['min_time']:
                timings[method]['min_time'] = elapsed_time
            timings[method]['total_time'] = timings[method]['total_time'] + elapsed_time
            timings[method]['avg_time'] = timings[method]['total_time'] / timings[method]['total_count']
        if data:
            timings[method]['data'][str(timings[method]['total_count'])] = data
    finally:
        timing_lock.release()

