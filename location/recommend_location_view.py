from django.http import JsonResponse

from utils.attributes import (
    error_invalid_request_method
)


def recommend_location_view(request):
    if request.method == 'GET':
        return JsonResponse({})
    else:
        return JsonResponse(error_invalid_request_method, status=405)
