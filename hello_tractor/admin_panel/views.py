from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from main.models import CustomUser
from sellers.models import Seller, Tractor
from .models import TractorBrand
from .forms import TractorBrandForm

@login_required
@staff_member_required
def admin_dashboard(request):
    users = CustomUser.objects.all().count()
    sellers = Seller.objects.all().count()
    tractors = Tractor.objects.all().count()

    context = {
        'users':users,
        'tractors': tractors,
        'sellers': sellers
    }
    return render(request, 'admin_panel/dashboard.html',context)

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
    users = CustomUser.objects.all()
    sellers = Seller.objects.all()
    tractors = Tractor.objects.all()
    if request.method == 'POST':
        form = TractorBrandForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            messages.success(request, "Brand added successfully!")
        else:
            messages.error(request, "There was an error adding the brand.")
    else:
        form = TractorBrandForm()

    # Include all existing brands for display
    brands = TractorBrand.objects.all()
    context = {
        'form': form,
        'brands': brands,
        'users':users,
        'tractors': tractors,
        'sellers': sellers
    }
    return render(request, 'admin_panel/admin_brands.html',context)

