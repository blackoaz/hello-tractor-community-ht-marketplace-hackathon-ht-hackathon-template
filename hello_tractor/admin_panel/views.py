from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

@login_required
@staff_member_required
def admin_dashboard(request):
    
    return render(request, 'admin_panel/dashboard.html')

@login_required
@staff_member_required
def admin_login(request):
    return render(request, 'admin_panel/login.html')


@login_required
@staff_member_required
def admin_sellers_dashboard(request):
    return render(request, 'admin_panel/admin_sellers.html')


@login_required
@staff_member_required
def admin_users_dashboard(request):
    return render(request, 'admin_panel/admin_users.html')


@login_required
@staff_member_required
def admin_tractors_dashboard(request):
    return render(request, 'admin_panel/admin_tractors.html')


@login_required
@staff_member_required
def admin_brands_dashboard(request):
    return render(request, 'admin_panel/admin_brands.html')

