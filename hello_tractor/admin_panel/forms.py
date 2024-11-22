from django import forms
from .models import TractorBrand
from main.mongo_db import fs

class TractorBrandForm(forms.ModelForm):
    image_file = forms.ImageField(label="Brand Logo/Image", required=False)

    class Meta:
        model = TractorBrand
        fields = ['brand_name', 'description']

    def save(self, commit=True):
        # Handle the MongoDB image storage and save metadata in the model
        image_file = self.cleaned_data.pop('image_file', None)
        brand = super().save(commit=False)

        if image_file:
            with image_file.open('rb') as f:
                metadata = {"brand_name": brand.brand_name, "category": "tractor_brand"}
                mongo_filename = fs.put(f, filename=image_file.name, metadata=metadata)
                brand.mongo_image_filename = mongo_filename  

        if commit:
            brand.save()
        return brand
