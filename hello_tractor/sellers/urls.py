from django.urls import path,include
from . import views

urlpatterns = [
    path('sellers/', views.dashboard, name='seller_dashboard'),
    path('accounts/', include('allauth.urls')),
]
