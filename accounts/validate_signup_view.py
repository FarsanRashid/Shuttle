import json
import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from service_layer import validate_signup
from service_layer.exceptions import VerificationFailed
from utils.attributes import (
    OTP,
    TOKEN,
    error_invalid_json,
    error_invalid_request_method,
    error_server_exception,
    success_signup_verification,
)
from utils.cache_factory import CacheFactory


logger = logging.getLogger(__name__)


@csrf_exempt
def validate_signup_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data.get(TOKEN)
            otp = data.get(OTP)

            cache_factory = CacheFactory()
            cache = cache_factory.get_cache()

            validate_signup.validate_signup(token, otp, cache)

            return JsonResponse(success_signup_verification, status=201)
        except json.JSONDecodeError:
            return JsonResponse(error_invalid_json, status=400)
        except validate_signup.InvalidPayload as e:
            return JsonResponse(e.args[0], status=400)
        except VerificationFailed as e:
            return JsonResponse(e.args[0], status=400)
        except Exception as e:
            logger.exception(e)
            return JsonResponse(error_server_exception, status=500)
    else:
        return JsonResponse(error_invalid_request_method, status=405)
