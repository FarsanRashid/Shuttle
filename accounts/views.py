from collections import namedtuple
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import redis
import jwt
import random
from .models import Passenger
from utils.response_attributes import (
    SUCCESS_SIGNUP_INITIATE,
    ERROR_MISSING_FIELD,
    ERROR_USERNAME_EXISTS,
    ERROR_INVALID_JSON,
    ERROR_INVALID_REQUEST_METHOD
)

PendingOtpValidation = namedtuple(
    'PendingOtpValidation', ['username', 'password', 'otp'])


@csrf_exempt
def initiate_signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return JsonResponse(ERROR_MISSING_FIELD, status=400)

            jwt_token = jwt.encode(
                {'username': username, }, 'secret', algorithm='HS256')

            redis_con = redis.Redis(host='localhost', port=6379, db=0)
            user = redis_con.get(jwt_token)
            if user is not None or Passenger.objects.filter(username=username).exists():
                return JsonResponse(ERROR_USERNAME_EXISTS, status=400)

            pending_otp_validation = PendingOtpValidation(
                username, password, random.randint(1000, 9999))

            redis_con.set(jwt_token,
                          json.dumps(pending_otp_validation._asdict()), ex=300)

            return JsonResponse(SUCCESS_SIGNUP_INITIATE, status=201)
        except json.JSONDecodeError:
            return JsonResponse(ERROR_INVALID_JSON, status=400)
    else:
        return JsonResponse(ERROR_INVALID_REQUEST_METHOD, status=405)
