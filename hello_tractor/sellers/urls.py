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
    path('logos/<str:file_id>/', views.serve_logo, name='serve_logo'),
    path('seller-registration/', views.SellerRegistrationView.as_view(), name='seller_registration'),
    path('register_new_tractor_for_sale/', views.register_new_tractor_for_sale, name='register_new_tractor_for_sale'),
    path('/tractor_detail/<str:uid>/', views.tractor_detail, name='tractor_detail'),
    path('image/<str:file_id>/', views.serve_image, name='serve_image'),
]
