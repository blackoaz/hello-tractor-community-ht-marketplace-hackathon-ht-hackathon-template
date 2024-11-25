from ..mongo_db import fs
from django.core.mail import send_mail

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
    

def forward_email_to_seller_from_customer(customer_name, email, customer_message, seller_email):
    """
    Forward the customer's message to the seller via email.
    """
    final_message = (
        f"Dear {seller_email},\n\n"
        f"You have received a message from a prospective customer via Hello Tractor:\n\n"
        f"Name: {customer_name}\n"
        f"Email: {email}\n"
        f"Message:\n{customer_message}\n\n"
        f"Please respond promptly to the customer's inquiry."
    )
    try:
        send_mail(
            subject=f"Hello Tractor: Message from {customer_name}",
            message=final_message,
            from_email=email,
            recipient_list=[seller_email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
