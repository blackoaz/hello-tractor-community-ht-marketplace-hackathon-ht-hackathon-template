from pymongo import MongoClient
from gridfs import GridFS

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['Tractor_App']
fs = GridFS(db)

# Save an image to MongoDB
import os
from gridfs import GridFS
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['tractor_app']
fs = GridFS(db)

def save_images_from_directory(directory_path):
    """
    Save all images from the specified directory into MongoDB GridFS, 
    only if they do not already exist.
    """
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            # Check if the file already exists in MongoDB
            if fs.find_one({"filename": filename}):
                print(f"File {filename} already exists in MongoDB. Skipping.")
                continue

            # Save file to GridFS
            with open(file_path, "rb") as f:
                fs.put(f, filename=filename)
                print(f"Saved {filename} to MongoDB.")

def get_image(filename):
    """
    Retrieve an image from MongoDB GridFS by filename.

    Args:
        filename (str): Name of the file to retrieve.

    Returns:
        Tuple: (binary image data, content type) or (None, None) if not found.
    """
    file = fs.find_one({"filename": filename})
    if file:
        return file.read(), file.content_type
    return None, None

