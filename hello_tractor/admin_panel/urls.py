from django.urls import path,include

# from hello_tractor.admin_panel import admin
from django.contrib import admin
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.admin_dashboard, name='admin_dashboard'),
    path('accounts/', include('allauth.urls')),
]
