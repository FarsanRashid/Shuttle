import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Passenger
from utils.response_attributes import (
    SUCCESS_SIGNUP,
    ERROR_MISSING_FIELD,
    ERROR_USERNAME_EXISTS,
    ERROR_INVALID_JSON,
    ERROR_INVALID_REQUEST_METHOD
)


@csrf_exempt
def initiate_signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return JsonResponse(ERROR_MISSING_FIELD, status=400)

            if Passenger.objects.filter(username=username).exists():
                return JsonResponse(ERROR_USERNAME_EXISTS, status=400)

            passenger = Passenger.objects.create_user(
                username=username, password=password)
            passenger.save()

            return JsonResponse(SUCCESS_SIGNUP, status=201)
        except json.JSONDecodeError:
            return JsonResponse(ERROR_INVALID_JSON, status=400)
    else:
        return JsonResponse(ERROR_INVALID_REQUEST_METHOD, status=405)
