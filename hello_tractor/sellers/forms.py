from django import forms
from .models import Tractor, TractorImage, Seller
from main.mongo_db import fs


# sellers registration form

class SellerRegistrationForm(forms.ModelForm):
    logo = forms.ImageField(required=False)

    class Meta:
        model = Seller
        fields = ['first_name', 'last_name', 'contact_number', 'contact_email', 'seller_description', 'logo']


class TractorForm(forms.ModelForm):
    class Meta:
        model = Tractor
        fields = ['tractor_name', 'model', 'year_of_manufucture', 'engine_capacity',
                  'price', 'location', 'condition', 'fuel_type', 'transmission']

class ImageUploadForm(forms.Form):
    image = forms.ImageField()


class TractorImageForm(forms.ModelForm):
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


