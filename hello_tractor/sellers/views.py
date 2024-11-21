from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from main.utils.utils import get_image_from_mongo
from .models import Tractor, TractorImage
from .forms import TractorForm, ImageUploadForm
from main.mongo_db import fs

def seller_login(request):
    return render(request, 'sellers/login.html')

def seller_logout(request):
    # Handle logout using django-allauth
    pass


def sellers_homepage(request):
    return render(request, 'sellers/sellers_homepage.html')

@login_required
def dashboard(request):
    if not request.user.is_seller:
        # return HttpResponseForbidden("You are not authorized")
        return redirect('sellers_homepage')
    return render(request, 'sellers/dashboard.html')




def add_tractor(request):
    if request.method == 'POST':
        tractor_form = TractorForm(request.POST)
        image_form = ImageUploadForm(request.POST, request.FILES)

        if tractor_form.is_valid() and image_form.is_valid():
            tractor = tractor_form.save()

            image_file = request.FILES['image']
            mongo_id = fs.put(image_file, filename=image_file.name, metadata={'tractor_uid': str(tractor.uid)})

            TractorImage.objects.create(tractor=tractor, mongo_filename=image_file.name)

            return redirect('homepage')

    else:
        tractor_form = TractorForm()
        image_form = ImageUploadForm()

    return render(request, 'add_tractor.html', {
        'tractor_form': tractor_form,
        'image_form': image_form
    })


def serve_tractor_image(request, tractor_id, image_id):
    """
    Retrieve and serve a specific tractor image by its mongo filename.
    """
    tractor = Tractor.objects.get(id=tractor_id)
    try:
        tractor_image = tractor.images.get(id=image_id)  # Get the tractor's image by its ID
        image_data = get_image_from_mongo(tractor_image.mongo_filename)
       
        if image_data:
            content_type = image_data.content_type
            return HttpResponse(image_data, content_type=content_type)  # Adjust the content_type based on the actual image type
    except TractorImage.DoesNotExist:
        return HttpResponse("Image not found", status=404)


