from django.utils.deprecation import MiddlewareMixin
from django_hosts import reverse

class DynamicRedirectMiddleware(MiddlewareMixin):
    """Middleware to dynamically handle LOGIN_REDIRECT_URL and LOGOUT_REDIRECT_URL."""
    
    def process_request(self, request):
        print(f"Request host: {request.get_host()}")  # This is the correct way to log the host
        
        # Use get_host() for both login and logout redirects
        if request.get_host() == 'admin.localhost:8000':
            request.LOGIN_REDIRECT_URL = reverse('admin_dashboard', host='admin')
            request.LOGOUT_REDIRECT_URL = reverse('admin_dashboard', host='admin')
            request.ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = reverse('admin_dashboard', host='admin')
            request.ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = reverse('admin_dashboard', host='admin')
        
        elif request.get_host() == 'sellers.localhost:8000':
            request.LOGIN_REDIRECT_URL = reverse('seller_dashboard', host='sellers')
            request.LOGOUT_REDIRECT_URL = reverse('seller_dashboard', host='sellers')
            request.ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = reverse('seller_dashboard', host='sellers')
            request.ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = reverse('seller_dashboard', host='sellers')
        
        else:
            request.LOGIN_REDIRECT_URL = reverse('homepage', host='main')
            request.LOGOUT_REDIRECT_URL = reverse('homepage', host='main')
            request.ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = reverse('homepage', host='main')
            request.ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = reverse('homepage', host='main')

