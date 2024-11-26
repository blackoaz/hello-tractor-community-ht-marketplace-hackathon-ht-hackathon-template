from django.urls import path, include
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('accounts/', include('allauth.urls')),
    path('administrator/',admin.site.urls),
    path('vehicle_details/<str:uid>', views.tractor_details, name='vehicle_details'),
    path('images/<str:filename>/', views.serve_image, name='serve_image'),
    path('images/<str:filename>/', views.serve_brand_image, name='serve_brand_image'),
    path('upload/', views.upload_image, name='upload_image'),
    path('filtered_tractors/', views.filtered_tractors, name='filtered_tractors'),
]
