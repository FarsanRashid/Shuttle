import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from service_layer.exceptions import InvalidPayload
from utils.attributes import (
    PASSWORD,
    USERNAME,
    error_invalid_json,
    error_invalid_request_method,
    error_missing_field,
)


def validate_payload(payload):
    if not all(payload):
        raise InvalidPayload(error_missing_field)


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get(USERNAME)
            password = data.get(PASSWORD)

            validate_payload((username, password))
            return JsonResponse({})

        except InvalidPayload as e:
            return JsonResponse(e.args[0], status=400)
        except json.JSONDecodeError:
            return JsonResponse(error_invalid_json, status=400)
    else:
        return JsonResponse(error_invalid_request_method, status=405)
