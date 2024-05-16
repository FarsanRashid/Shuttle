from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        return JsonResponse({'message': 'User created successfully'}, status=201)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
