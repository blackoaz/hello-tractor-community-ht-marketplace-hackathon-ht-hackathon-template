from django.urls import path,include
from . import views

urlpatterns = [
    path('sellers/', views.dashboard, name='seller_dashboard'),
    path('accounts/', include('allauth.urls')),
    path('add-tractor/', views.add_tractor, name='add_tractor'),
    path('images/<str:tractor_uid>/<str:filename>/', views.serve_tractor_image, name='serve_tractor_image'),

]
