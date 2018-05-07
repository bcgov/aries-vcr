
"""
A collection of utility classes for TOB
"""

import os
from django.conf import settings


#
# Read settings from a custom settings file 
# based on the path provided as an input parameter
# The choice of the custom settings file is drived by the value of the TOB_THEME env
# variables (i.e. ongov)
#
def fetch_custom_settings(*settings):
    _fields = ()
    if not settings.CUSTOMIZATIONS:
        return _fields

    _dict = settings.CUSTOMIZATIONS.items()
    for key, value in _dict:
        _dict = value;
        if not value is dict:
            _fields = value
            break

    
    return _fields
         

