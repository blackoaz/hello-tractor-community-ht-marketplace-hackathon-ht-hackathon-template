from pymongo import MongoClient
from pymongo.server_api import ServerApi
from gridfs import GridFS
import os

from admin_panel.models import TractorBrand
from pymongo.errors import DuplicateKeyError

# # Connect to MongoDB
# client = MongoClient(
#     'mongodb+srv://${MONGO_USER}:{MONGO_PASSWORD}@hellotractor.sna2a.mongodb.net/?retryWrites=true&w=majority&appName=HelloTractor'
# )
# db = client['tractor_app']
# fs = GridFS(db)

uri = (
    f"mongodb+srv://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWORD')}"
    "@hellotractor.sna2a.mongodb.net/?retryWrites=true&w=majority&appName=HelloTractor"
)

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['tractor_app']
fs = GridFS(db)

# Test the connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"Connection failed: {e}")

# client = MongoClient("mongodb://${MONGO_USER}:${MONGO_PASSWORD}@mongoDb:27017/")
# db = client['tractor_app']
# fs = GridFS(db)


def save_images_from_directory(directory_path, brand_name):
    """
    Save all images from the specified directory into MongoDB GridFS, 
    associating them with a tractor brand, if they don't already exist.
    """
    try:
        brand = TractorBrand.objects.get(name=brand_name)
    except TractorBrand.DoesNotExist:
        print(f"Brand '{brand_name}' does not exist. Please create it first.")
        return

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            # Check if the file already exists in MongoDB
            if fs.find_one({"filename": filename, "metadata.brand": brand_name}):
                print(f"File {filename} already exists for brand {brand_name}. Skipping.")
                continue

            with open(file_path, "rb") as f:
                metadata = {
                    "category": "tractor_brand",
                    "filename": filename,
                    "brand": brand_name,
                }
                try:
                    fs.put(f, filename=filename, metadata=metadata)
                    print(f"Saved {filename} to MongoDB for brand {brand_name}.")
                except DuplicateKeyError:
                    print(f"Duplicate file detected: {filename}. Skipping.")


def get_image(filename):
    """
    Retrieve an image from MongoDB GridFS by filename and category.

    Args:
        filename (str): Name of the file to retrieve.

    Returns:
        Tuple: (binary image data, content type) or (None, None) if not found.
    """
    # Fetch the image with the category "tractor_brand"
    file = fs.find_one({"filename": filename, "metadata.category": "tractor_brand"})
    if file:
        return file.read(), file.content_type
    return None, None

