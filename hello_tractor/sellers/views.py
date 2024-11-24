from bson import ObjectId
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator

from main.utils.utils import get_image_from_mongo, handle_mongo_tractor_for_sale_upload
from .models import LogoImage, Seller, Tractor, TractorImage
from .forms import SellerRegistrationForm, TractorForm, ImageUploadForm
from main.mongo_db import fs


# Homepage section for sellers
def sellers_homepage(request):
    is_a_registered_seller = False
    try:
        seller = Seller.objects.get(user=request.user)
        is_a_registered_seller = True
    except Seller.DoesNotExist:
        pass
    context = {
        'is_a_registered_seller': is_a_registered_seller
    }
    
    return render(request, 'sellers/sellers_homepage.html',context)

# Dashboard section for sellers
@login_required
def dashboard(request):
    if not request.user.is_seller:
        return redirect('sellers_homepage')
    else:
        pass
    return render(request, 'sellers/dashboard.html')


# Seller registration view
@method_decorator(login_required, name='dispatch')
class SellerRegistrationView(View):
    def get(self, request):
        form = SellerRegistrationForm()
        return render(request, 'sellers/sellers_registration.html', {'form': form})

    def post(self, request):
        if request.user.is_seller:
            messages.info(request, "You are already registered as a seller!")
            return redirect('seller_dashboard')
        elif Seller.objects.filter(user=request.user).exists():
            messages.error(request, "You are already a registered seller but your acount is not active")
            return redirect('seller_dashboard')
        else:
            form = SellerRegistrationForm(request.POST, request.FILES)
            print(form.is_valid())
            if form.is_valid():
                print('form is valid! saving it')
                name = form.cleaned_data.get('first_name')
                print(name)
                seller = form.save(commit=False)
                seller.user = request.user 
                seller.save()
                print('seller added successfully: ',seller.uid)
                # Save the logo to GridFS
                logo_file = request.FILES['logo']
                metadata = {'seller_logo_uid': str(seller.uid),'category': 'seller_logo'}
                print('metadata: ',metadata)
                file_id = fs.put(logo_file, filename=logo_file.name, content_type=logo_file.content_type, metadata=metadata)

                # Save the LogoImage reference
                LogoImage.objects.create(logo=seller, mongo_filename=str(file_id))

                messages.success(request, "Seller registered successfully!")
                print('seller added successfully: ',seller.uid)
                return redirect('seller_dashboard')  # Redirect to the seller's dashboard
            else:
                return render(request, 'sellers/sellers_registration.html', {'form': form})
        

def serve_logo(request, file_id):
    try:
        file = fs.get(file_id)
        response = HttpResponse(file.read(), content_type=file.content_type)
        response['Content-Disposition'] = f'inline; filename="{file.filename}"'
        return response
    except Exception as e:
        return HttpResponse(status=404)



@login_required
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
        tractor_image = tractor.images.get(id=image_id)
        image_data = get_image_from_mongo(tractor_image.mongo_filename)
       
        if image_data:
            content_type = image_data.content_type
            return HttpResponse(image_data, content_type=content_type)
    except TractorImage.DoesNotExist:
        return HttpResponse("Image not found", status=404)
    

def serve_image(request, file_id):
    """
    Serve an image from MongoDB GridFS.
    Args:
        file_id (str): The GridFS file ID.
    Returns:
        FileResponse: The image response.
    """
    try:
        grid_out = fs.get(ObjectId(file_id))
        response = HttpResponse(grid_out, content_type=grid_out.content_type)
        response['Content-Disposition'] = f'inline; filename="{grid_out.filename}"'
        return response
    except Exception as e:
        return HttpResponse(f"Error: {e}", status=404)
    

# view function for adding a new tractor
@login_required
def register_new_tractor_for_sale(request):
    """
    This view function allows a seller to register a new tractor for sale.
    The form includes fields for the tractor details and multiple image uploads.
    """
    if request.user.is_seller:
        try:
            seller_instance = Seller.objects.get(user=request.user)
            print("Seller Instance: ",seller_instance)
        except Seller.DoesNotExist:
            return HttpResponse("Seller profile not found.", status=404)

        if request.method == "POST":
            tractor_form = TractorForm(request.POST)
            image_form = ImageUploadForm(request.POST, request.FILES)
            # image_file = request.FILES['image']
            # mongo_id = fs.put(image_file, filename=image_file.name, metadata={'tractor_uid': str(tractor.uid)})


            if tractor_form.is_valid() and image_form.is_valid():
                tractor_instance = tractor_form.save(commit=False)
                tractor_instance.tractor_seller = seller_instance
                tractor_instance.save()

                # Save associated images
                images = request.FILES.getlist('images')
                for image in images:
                    TractorImage.objects.create(
                        tractor=tractor_instance,
                        mongo_filename=handle_mongo_tractor_for_sale_upload(image, tractor_instance)
                    )

                return redirect('tractor_detail', pk=tractor_instance.uid)

        else:
            tractor_form = TractorForm()
            image_form = ImageUploadForm()

    context = {
        'tractor_form': tractor_form,
        'image_form': image_form,
    }
    return render(request,'sellers/register_tractor_sale.html',context)


def tractor_detail(request, pk):
    """
    View Function for displaying newly registerd tractors.
    """
    tractor = Tractor.objects.get(uid=pk)
    images = []

    # Fetch images from MongoDB
    for image in tractor.images.all():
        image_data = get_image_from_mongo(image.mongo_filename)
        if image_data:
            images.append({
                'data': image_data,
                'name': image.mongo_filename
            })

    return render(request, 'sellers/registered_tractor_details.html', {'tractor': tractor, 'images': images})



