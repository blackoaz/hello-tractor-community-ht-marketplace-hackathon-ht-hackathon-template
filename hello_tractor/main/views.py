from django.shortcuts import redirect, render
from django.http import HttpResponse
from pathlib import Path
from .mongo_db import fs
from sellers.models import Tractor
from django.db.models import F 
from admin_panel.models import TractorBrand

def homepage(request):
    """
    This is the main view function for the homepage,
    takes in all the featured sales and logos for display
    """
    # Fetch all tractors available for sale
    featured_tractors = Tractor.objects.filter(
        is_available=True, is_featured=True
    ).order_by('-is_featured', '-created').annotate(
        seller_name=F('tractor_seller__user__username')
    )

    # Fetching tractor brand images
    image_files = fs.find({"metadata.category": "tractor_brand"})
    images = [file.filename for file in image_files]

    tractor_list = []
    for tractor in featured_tractors:
        # Fetch the image associated with the tractor from GridFS
        file = fs.find_one({'metadata.tractor_uid': str(tractor.uid)})
        image_url = f"/images/{file.filename}" if file else None 

        tractor_list.append({
            'uid': tractor.uid,
            'name': tractor.tractor_name,
            'model': tractor.model,
            'location': tractor.location,
            'price': tractor.price,
            'condition': tractor.condition,
            'seller_name': tractor.tractor_seller,
            'transmission': tractor.transmission,
            'fuel_type': tractor.fuel_type,
            'image_url': image_url,
            'is_featured': tractor.is_featured,
            'created': tractor.created,
        })

    context = {'tractors': tractor_list,'images':images}
    return render(request, 'main/homepage.html', context)



# view function for filtered tractors
def filtered_tractors(request):
    """
    View function for enabling users to filter tractors based on differnt
    categoroies and preferences.
    """
    brands = TractorBrand.objects.all()
    tractors = Tractor.objects.all()

    brand = request.GET.get('brand')
    if brand:
        tractors = tractors.filter(model__icontains=brand)

    condition = request.GET.get('condition')
    if condition:
        tractors = tractors.filter(condition__icontains=condition)

    transmission = request.GET.get('transmission')
    if transmission:
        tractors = tractors.filter(transmission__icontains=transmission)

    fuel = request.GET.get('fuel')
    if fuel:
        tractors = tractors.filter(fuel_type__icontains=fuel)

    year = request.GET.get('year')
    if year:
        tractors = tractors.filter(year=year)

    price = request.GET.get('price')
    if price:
        tractors = tractors.filter(price__lte=price)
    context={'tractors': tractors, 'brands':brands}
    print(tractors)
    return render(request, 'main/filtered_tractors.html',context=context)

# view function for serving tractor brand images
def serve_image(request, filename):
    """
    Function for retrieving image from MongoDb,
    parameter(filename)
    """
    print(f"Serving image: {filename}")
    file = fs.find_one({"filename": filename})
    if file:
        return HttpResponse(file.read(), content_type=file.content_type)
    print(f"Image not found: {filename}")
    return HttpResponse("Image not found", status=404)

def serve_brand_image(request, filename):
    """
    Serve an image from MongoDB GridFS by filename and filter by category (tractor brand).
    """
    # Fetch the image with the category "tractor_brand"
    file = fs.find_one({"filename": filename, "metadata.category": "tractor_brand"})
    
    if file:
        
        image_data = file.read()
        content_type = file.content_type
        
        return HttpResponse(image_data, content_type=content_type)
    
    return HttpResponse("Image not found", status=404)

# view function for uploading images
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_file = request.FILES['image']
        
        if fs.find_one({"filename": uploaded_file.name}):
            return HttpResponse("Image with this name already exists.", status=400)
        
        fs.put(uploaded_file, filename=uploaded_file.name)
        print(f"Uploaded {uploaded_file.name} to MongoDB.")

        return redirect('homepage')

    return HttpResponse("Invalid request", status=400)


# view function for vehicle_details
def vehicle_details(request, uid):
    return render(request, 'main/vehicle_details.html', {'uid': uid})

