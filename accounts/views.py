import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Passenger
from utils.errors import ERROR_INVALID_JSON, ERROR_INVALID_REQUEST, ERROR_MISSING_FIELD, ERROR_USERNAME_EXISTS


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return JsonResponse({'error': ERROR_MISSING_FIELD}, status=400)

            if Passenger.objects.filter(username=username).exists():
                return JsonResponse({'error': ERROR_USERNAME_EXISTS}, status=400)

            passenger = Passenger.objects.create_user(
                username=username, password=password)
            passenger.save()

            return JsonResponse({'message': 'User created successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': ERROR_INVALID_JSON}, status=400)
    else:
        return JsonResponse({'error': ERROR_INVALID_REQUEST}, status=405)
