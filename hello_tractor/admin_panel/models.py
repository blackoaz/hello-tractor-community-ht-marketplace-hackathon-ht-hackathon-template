from django.db import models

# Create your models here.

class TractorBrand(models.Model):
    brand_name = models.CharField(max_length=100, unique=True) 
    description = models.TextField(blank=True, null=True)  
    mongo_image_filename = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.brand_name
