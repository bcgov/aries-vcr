
import json

from django.http import HttpResponse
from django.shortcuts import render
from api.models.VOClaim import VOClaim

def health(request):
    """
    Health check for OpenShift
    """
    return HttpResponse(VOClaim.objects.count())