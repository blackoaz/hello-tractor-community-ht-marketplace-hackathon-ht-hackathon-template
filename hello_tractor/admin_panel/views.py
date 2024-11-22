from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TractorBrand
from .forms import TractorBrandForm

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
    }
    return render(request, 'admin_panel/admin_brands.html')

