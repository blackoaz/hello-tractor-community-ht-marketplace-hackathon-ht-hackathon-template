from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse

def seller_login(request):
    return render(request, 'sellers/login.html')

def seller_logout(request):
    # Handle logout using django-allauth
    pass

@login_required
def dashboard(request):
    if not request.user.groups.filter(name='Sellers').exists():
        return HttpResponseForbidden('You are not authorized to view this page')
    return render(request, 'sellers/dashboard.html')

