import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import redis

from service_layer import validate_signup
from utils.attributes import (
    OTP,
    TOKEN,
    error_invalid_request_method,
    error_server_exception,
)
from utils.config import REDIS_HOST, REDIS_PORT


@csrf_exempt
def validate_signup_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data.get(TOKEN)
            otp = data.get(OTP)

            validate_signup.validate_signup(token, otp, redis.Redis(
                host=REDIS_HOST, port=REDIS_PORT, decode_responses=True))

            return JsonResponse({"test": "test"}, status=200)
        except validate_signup.InvalidPayload as e:
            return JsonResponse(e.args[0], status=400)
        except Exception:
            return JsonResponse(error_server_exception, status=500)
    else:
        return JsonResponse(error_invalid_request_method, status=405)
