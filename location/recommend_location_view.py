from django.http import JsonResponse

from utils.attributes import (
    error_invalid_request_method,
    error_missing_paramater
)


def recommend_location_view(request):
    if request.method == 'GET':
        if request.GET.get('q') is None:
            return JsonResponse(error_missing_paramater, status=400)
        if request.user.is_authenticated is False:
            return JsonResponse({}, status=401)
        return JsonResponse({}, status=200)
    else:
        return JsonResponse(error_invalid_request_method, status=405)
