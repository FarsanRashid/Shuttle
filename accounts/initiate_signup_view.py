import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import redis

from service_layer import services
from utils.attributes import (
    CONTACT_NUMBER,
    COUNTRY_DIAL_CODE,
    PASSWORD,
    TOKEN,
    USERNAME,
    error_invalid_json,
    error_invalid_request_method,
    error_server_exception,
    error_username_exists,
    success_signup_initiate,
)
from utils.config import REDIS_HOST, REDIS_PORT


@csrf_exempt
def initiate_signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get(USERNAME)
            password = data.get(PASSWORD)
            country_dial_code = data.get(COUNTRY_DIAL_CODE)
            contact_number = data.get(CONTACT_NUMBER)

            jwt_token = services.initate_signup(username,
                                                password, country_dial_code,
                                                contact_number,
                                                redis.Redis(
                                                    host=REDIS_HOST, port=REDIS_PORT,
                                                    decode_responses=True))

            success_signup_initiate[TOKEN] = jwt_token
            return JsonResponse(success_signup_initiate, status=201)

        except services.InvalidPayload as e:
            return JsonResponse(e.args[0], status=400)
        except services.UserNameNotUnique:
            return JsonResponse(error_username_exists, status=400)
        except json.JSONDecodeError:
            return JsonResponse(error_invalid_json, status=400)
        except Exception:
            return JsonResponse(error_server_exception, status=500)
    else:
        return JsonResponse(error_invalid_request_method, status=405)
