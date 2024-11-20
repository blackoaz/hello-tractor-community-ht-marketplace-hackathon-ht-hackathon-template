from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('accounts/', include('allauth.urls')),
    path('vehicle_details/<str:uid>', views.vehicle_details, name='vehicle_details'),
    path('images/<str:filename>/', views.serve_image, name='serve_image'),
    path('images/<str:filename>/', views.serve_brand_image, name='serve_brand_image'),
    path('upload/', views.upload_image, name='upload_image'),
]
