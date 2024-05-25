from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from utils.attributes import error_invalid_request_method


@csrf_exempt
def validate_signup(request):
    if request.method == 'POST':
        pass
    else:
        return JsonResponse(error_invalid_request_method, status=405)
