import logging

from django.http import JsonResponse

from service_layer import recommend_location
from utils.attributes import (
    error_invalid_request_method,
    error_invalid_token,
    error_missing_paramater,
    error_server_exception,
    error_query_string_too_short,
    success_location_recommended,
)
from utils.location_service_provider import LocationServiceProvider

logger = logging.getLogger(__name__)


def recommend_location_view(request):
    if request.method == 'GET':
        if request.GET.get('q') is None:
            return JsonResponse(error_missing_paramater, status=400)
        if request.user.is_authenticated is False:
            return JsonResponse(error_invalid_token, status=401)
        try:
            location_service = LocationServiceProvider().get_provider()
            recommendations = recommend_location.recommend(
                request.GET.get('q'), location_service)
        except recommend_location.SearchQueryTooShortError as e:
            return JsonResponse(error_query_string_too_short, status=400)
        except Exception as e:
            logger.exception(e)
            return JsonResponse(error_server_exception, status=500)
        return JsonResponse(recommendations | success_location_recommended, status=200)
    else:
        return JsonResponse(error_invalid_request_method, status=405)
