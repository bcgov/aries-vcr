from django.http import HttpResponse

from api.v2.models.Issuer import Issuer


def health(request):
    """
    Health check for OpenShift
    """
    return HttpResponse(Issuer.objects.count())
