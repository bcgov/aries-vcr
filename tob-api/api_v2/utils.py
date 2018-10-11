
"""
A collection of utility classes for TOB
"""

import os
from django.conf import settings
from django.db import connection

#
# Read settings from a custom settings file
# based on the path provided as an input parameter
# The choice of the custom settings file is driven by the value of the TOB_THEME env
# variable (i.e. ongov)
#


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
            [model_cls._meta.db_table])
        row = cursor.fetchone()
    finally:
        if close:
            cursor.close()
    return row[0]
