### views.py ###
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseServerError

import random
import json


@csrf_exempt
def echo_view(request):
    if request.method == 'POST':
        post_data = request.body
        print(post_data)
        return JsonResponse({"thanks": "you"})

    return JsonResponse({"method": "notsupported"})


@csrf_exempt
def error_view(request):
    if request.method == 'POST':
        post_data = request.body
        print(post_data)
        data = json.loads(post_data)
        if "subscription" in data and "test" in data["subscription"]:
            return JsonResponse({"thanks": "you"})
        else:
            return HttpResponseServerError()

    return JsonResponse({"method": "notsupported"})


@csrf_exempt
def random_view(request):
    if request.method == 'POST':
        post_data = request.body
        print(post_data)
        data = json.loads(post_data)
        if "subscription" in data and "test" in data["subscription"]:
            return JsonResponse({"thanks": "you"})
        else:
            if 0.5 < random.random():
                return JsonResponse({"thanks": "you"})
            else:
                return HttpResponseServerError()

    return JsonResponse({"method": "notsupported"})

