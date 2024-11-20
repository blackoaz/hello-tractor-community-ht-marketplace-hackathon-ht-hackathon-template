from django.shortcuts import redirect, render
from django.http import HttpResponse
from pathlib import Path
from .mongo_db import get_image, save_images_from_directory,fs



def homepage(request):
    # # Save images from directory to MongoDB (optional)
    # image_path = Path(__file__).resolve().parent.parent / "static/images/brands"
    # # for file in fs.find():
    # #     print(f"Deleting file: {file.filename}")
    # #     fs.delete(file._id)
    
    # save_images_from_directory(image_path)
    image_files = fs.find()  # Get all files in GridFS
    images = [file.filename for file in image_files]


    # Pass the image filenames to the template
    context = {
        "images": images,
    }
    return render(request, 'main/homepage.html', context)

# view function for serving tractor brand images
def serve_image(request, filename):
    """
    Serve an image from MongoDB GridFS by filename.
    """
    file = fs.find_one({"filename": filename})
    if file:
        return HttpResponse(file.read(), content_type=("image/jpeg",'image/png','image/webp','image/jpg'))
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

# # view function for serving tractor brand images
# def serve_image(request, filename):
#     image_data = get_image(filename)
#     if image_data:
#         return HttpResponse(image_data, content_type=("image/jpeg",'image/png','image/webp','image/jpg')) 
#     return HttpResponse("Image not found", status=404)


