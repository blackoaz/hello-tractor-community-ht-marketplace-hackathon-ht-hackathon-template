from ..mongo_db import fs

def get_image_from_mongo(mongo_filename):
    """
    Retrieve the image file from MongoDB by its GridFS filename (file_id).
    """
    file = fs.get(mongo_filename)
    if file:
        return file.read()
    return None

def handle_mongo_tractor_for_sale_upload(image, tractor):
    """
    Save the uploaded image to MongoDB and return the GridFS filename.
    Args:
        image (File): The uploaded image file.
        tractor (Tractor): The tractor instance associated with the image.
    Returns:
        str: The GridFS file ID.
    """
    file_id = fs.put(image, filename=image.name, metadata={
        "category": "tractor",
        "tractor_uid": str(tractor.uid) 
    })
    return str(file_id)


def get_image_from_mongo(file_id):
    """
    Retrieve an image from MongoDB GridFS by file_id.
    Args:
        file_id (str): The GridFS file ID.
    Returns:
        bytes: The image data.
    """
    try:
        grid_out = fs.get(file_id)
        return grid_out.read()
    except Exception as e:
        print(f"Error retrieving image: {e}")
        return None

