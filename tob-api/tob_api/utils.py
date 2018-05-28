
"""
A collection of utility classes for TOB
"""

import os
from django.conf import settings

#
# Read settings from a custom settings file 
# based on the path provided as an input parameter
# The choice of the custom settings file is driven by the value of the TOB_THEME env
# variable (i.e. ongov)
#

def fetch_custom_settings(*args):
    _values = {}

    if not hasattr(settings, 'CUSTOMIZATIONS'):
        return _values

    _dict = settings.CUSTOMIZATIONS
    for arg in args:
        if not _dict[arg]:
            return _values
        _dict = _dict[arg]

    return _dict