from django import forms
from .models import Sellers_Emails, Tractor, TractorImage, Seller
from main.mongo_db import fs


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


# sellers registration form
class SellerRegistrationForm(forms.ModelForm):
    """
    Form for registring a new customer as a seller on Hello Tractor platform
    """
    logo = forms.ImageField(required=False)

    class Meta:
        model = Seller
        fields = ['first_name', 'last_name', 'contact_number', 'contact_email', 'seller_description', 'logo']


class TractorForm(forms.ModelForm):
    """
    Form for registering a new tractor that the user wants to advertise 
    on hello tractor platform
    """
    class Meta:
        model = Tractor
        fields = ['tractor_name', 'model', 'year_of_manufucture', 'engine_capacity',
                  'price', 'location', 'condition', 'fuel_type', 'transmission','Tractor_description',
                  'Wheel_Drive','horse_power','Number_of_cylinders','mileage','forward_speed',
                  'reverse_speed','lifting_capacity','is_featured','is_available']


class ImageUploadForm(forms.Form):
    """
    A form for taking user uploaded images and storing in MongoDb,
    The seller can add multiple images
    """
    images = MultipleFileField(label='Select files', required=True)


class TractorImageForm(forms.ModelForm):
    """
    Form for Uploading Tractor images on the Admin section
    """
    image_file = forms.ImageField()

    class Meta:
        model = TractorImage
        fields = ['tractor', 'mongo_filename', 'image_file']

    def save(self, commit=True):
        image = self.cleaned_data['image_file']  # Get the uploaded image file
        tractor = self.cleaned_data.get('tractor')  # Get the associated tractor instance

        if not tractor:
            raise ValueError("Tractor instance is required to save the image.")

        # Save image to GridFS with metadata linking it to the tractor
        file_id = fs.put(image, filename=image.name, metadata={"category": "tractor", "tractor_uid": str(tractor.uid)})

        # Save the file ID into the `mongo_filename` field of TractorImage
        tractor_image = super().save(commit=False)
        tractor_image.mongo_filename = str(file_id)

        if commit:
            tractor_image.save()
        
        return tractor_image
    

class CustomerMessageForm(forms.ModelForm):
    class Meta:
        model = Sellers_Emails
        fields = ['customer_name', 'email', 'customer_message']


