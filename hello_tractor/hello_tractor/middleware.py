import os
from django.utils.deprecation import MiddlewareMixin
from django_hosts import reverse

class DynamicRedirectMiddleware(MiddlewareMixin):
    """Middleware to dynamically handle LOGIN_REDIRECT_URL and LOGOUT_REDIRECT_URL."""

    def process_request(self, request):
        # Get environment variables
        debug_mode = os.getenv("DEBUG", "False").lower() in ("true", "1")
        base_url = os.getenv("BASE_URL", "localhost:8000")
        prod_url = os.getenv("BASE_URL_PROD", "").strip()

        # Determine the appropriate base URL based on DEBUG mode
        # current_base_url = base_url if debug_mode else prod_url # temporary measure to deploy in render
        current_base_url = prod_url
        current_host = request.get_host()

        print(f"Request host: {current_host}")
        print(f"DEBUG mode: {debug_mode}, Base URL: {current_base_url}")

        # Define redirect URLs based on the host
        if current_host == f'admin.{current_base_url}':
            request.LOGIN_REDIRECT_URL = reverse('admin_dashboard', host='admin')
            request.LOGOUT_REDIRECT_URL = reverse('admin_dashboard', host='admin')
            request.ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = reverse('admin_dashboard', host='admin')
            request.ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = reverse('admin_dashboard', host='admin')

        elif current_host == f'sellers.{current_base_url}':
            request.LOGIN_REDIRECT_URL = reverse('seller_dashboard', host='sellers')
            request.LOGOUT_REDIRECT_URL = reverse('seller_dashboard', host='sellers')
            request.ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = reverse('seller_dashboard', host='sellers')
            request.ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = reverse('seller_dashboard', host='sellers')

        else:  # Default to the main host
            request.LOGIN_REDIRECT_URL = reverse('homepage', host='main')
            request.LOGOUT_REDIRECT_URL = reverse('homepage', host='main')
            request.ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = reverse('homepage', host='main')
            request.ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = reverse('homepage', host='main')
