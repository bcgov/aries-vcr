from django.http import HttpResponse, JsonResponse
from api.models import WalletItem

def health(request):
    """
    Health check for OpenShift
    """
    return HttpResponse(WalletItem.objects.count())
