import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Passenger


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            if Passenger.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)

            passenger = Passenger.objects.create_user(
                username=username, password=password)
            passenger.save()

            return JsonResponse({'message': 'User created successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
