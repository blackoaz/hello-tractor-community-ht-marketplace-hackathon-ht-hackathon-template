from ..mongo_db import fs

def get_image_from_mongo(mongo_filename):
    """
    Retrieve the image file from MongoDB by its GridFS filename (file_id).
    """
    file = fs.get(mongo_filename)
    if file:
        return file.read()
    return None
