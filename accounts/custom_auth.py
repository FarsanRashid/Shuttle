from accounts.models import TokenStore


class CustomAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # Get credentials from request (replace 'X-API-KEY' with your header name)
            auth_header = request.META.get('HTTP_AUTHORIZATION')

            if auth_header:
                # Extract credentials (assuming API key based authentication)
                api_key = auth_header.strip()
                # Authenticate using the API key (replace with your logic)
                result = TokenStore.objects.get(key=api_key)

                if result:
                    # Set user on the request object
                    request.user = result.user

        except Exception:
            pass

        response = self.get_response(request)
        return response
