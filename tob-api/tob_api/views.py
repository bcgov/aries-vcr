
import json

from django.http import HttpResponse
from django.shortcuts import render
from api.models.VerifiableClaim import VerifiableClaim

def health(request):
    """
    Health check for OpenShift
    """
    return HttpResponse(VerifiableClaim.objects.count())