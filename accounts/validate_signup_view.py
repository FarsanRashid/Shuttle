import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from adapters.cache import RedisCache
from service_layer import validate_signup
from service_layer.exceptions import VerificationFailed
from utils.attributes import (
    OTP,
    TOKEN,
    error_invalid_request_method,
    error_server_exception,
    error_invalid_json,
    success_signup_verification
)


@csrf_exempt
def validate_signup_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data.get(TOKEN)
            otp = data.get(OTP)

            validate_signup.validate_signup(token, otp, RedisCache())

            return JsonResponse(success_signup_verification, status=201)
        except json.JSONDecodeError:
            return JsonResponse(error_invalid_json, status=400)
        except validate_signup.InvalidPayload as e:
            return JsonResponse(e.args[0], status=400)
        except VerificationFailed as e:
            return JsonResponse(e.args[0], status=400)
        except Exception:
            return JsonResponse(error_server_exception, status=500)
    else:
        return JsonResponse(error_invalid_request_method, status=405)
