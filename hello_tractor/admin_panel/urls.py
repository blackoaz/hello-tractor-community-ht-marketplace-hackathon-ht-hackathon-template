from django.urls import path,include
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('administrator/',admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('admin_sellers/', views.admin_sellers_dashboard, name='admin_sellers_dashboard'),
    path('admin_users/', views.admin_users_dashboard, name='admin_users_dashboard'),
    path('admin_tractors/', views.admin_tractors_dashboard, name='admin_tractors_dashboard'),
    path('admin_brands/', views.admin_brands_dashboard, name='admin_brands_dashboard'),
]
