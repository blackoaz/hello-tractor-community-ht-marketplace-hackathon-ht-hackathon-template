from django.urls import path,include
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.dashboard, name='seller_dashboard'),
    path('sellers/', views.dashboard, name='seller_dashboard'),
    path('accounts/', include('allauth.urls')),
    path('administrator/',admin.site.urls),
    path('add-tractor/', views.add_tractor, name='add_tractor'),
    path('sellers_homepage/', views.sellers_homepage, name='sellers_homepage'),
    path('images/<str:tractor_uid>/<str:filename>/', views.serve_tractor_image, name='serve_tractor_image'),

]
