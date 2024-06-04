import json
import logging

from django.contrib.auth import authenticate, login
from django.http import JsonResponse

from service_layer.exceptions import InvalidPayload
from utils.attributes import (
    PASSWORD,
    SESSION_ID,
    USERNAME,
    error_invalid_credentials,
    error_invalid_json,
    error_invalid_payload,
    error_invalid_request_method,
    error_server_exception,
    success_login,
)

logger = logging.getLogger(__name__)


def validate_payload(payload):
    if not all(isinstance(value, str)
               for value in payload):
        raise InvalidPayload(error_invalid_payload)


def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get(USERNAME)
            password = data.get(PASSWORD)

            validate_payload((username, password))
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                session_id = request.session.session_key
                success_login[SESSION_ID] = session_id
                return JsonResponse(success_login)
            else:
                return JsonResponse(error_invalid_credentials, status=401)

        except InvalidPayload as e:
            return JsonResponse(e.args[0], status=400)
        except json.JSONDecodeError:
            return JsonResponse(error_invalid_json, status=400)
        except Exception as e:
            logger.exception(e)
            return JsonResponse(error_server_exception, status=500)
    else:
        return JsonResponse(error_invalid_request_method, status=405)
