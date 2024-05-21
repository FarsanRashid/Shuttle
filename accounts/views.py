import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import redis

from service_layer import services
from utils.config import REDIS_HOST, REDIS_PORT
from utils.response_attributes import (
    ERROR_INVALID_JSON,
    ERROR_INVALID_REQUEST_METHOD,
    ERROR_MISSING_FIELD,
    ERROR_USERNAME_EXISTS,
    SUCCESS_SIGNUP_INITIATE,
)


@csrf_exempt
def initiate_signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            services.initate_signup(username, password, redis.Redis(
                host=REDIS_HOST, port=REDIS_PORT, decode_responses=True))

            return JsonResponse(SUCCESS_SIGNUP_INITIATE, status=201)

        except services.InvalidPayload:
            return JsonResponse(ERROR_MISSING_FIELD, status=400)
        except services.UserNameNotUnique:
            return JsonResponse(ERROR_USERNAME_EXISTS, status=400)
        except json.JSONDecodeError:
            return JsonResponse(ERROR_INVALID_JSON, status=400)
    else:
        return JsonResponse(ERROR_INVALID_REQUEST_METHOD, status=405)
