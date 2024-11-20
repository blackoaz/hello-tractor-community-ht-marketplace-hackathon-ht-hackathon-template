from django.utils.deprecation import MiddlewareMixin
from django_hosts import reverse

class DynamicRedirectMiddleware(MiddlewareMixin):
    """Middleware to dynamically handle LOGIN_REDIRECT_URL and LOGOUT_REDIRECT_URL."""
    
    def process_request(self, request):
        if request.get_host() == 'admin.localhost:8000':
            request.LOGIN_REDIRECT_URL = reverse('admin_dashboard', host='admin')
            request.LOGOUT_REDIRECT_URL = reverse('admin_dashboard', host='admin')
        elif request.get_host() == 'sellers.localhost:8000':
            request.LOGIN_REDIRECT_URL = reverse('seller_dashboard', host='sellers')
            request.LOGOUT_REDIRECT_URL = reverse('seller_dashboard', host='sellers')
        else:
            request.LOGIN_REDIRECT_URL = reverse('homepage', host='main')
            request.LOGOUT_REDIRECT_URL = reverse('homepage', host='main')
