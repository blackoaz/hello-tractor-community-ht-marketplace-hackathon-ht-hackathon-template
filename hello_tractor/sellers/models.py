from django.db import models
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_delete


from main.models import CustomUser,Common
from main.mongo_db import fs

# Create your models here.
class Seller(Common):
    """
    Model for registering a seller into the system
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact_number = PhoneNumberField(blank=False, null=False)
    contact_email = models.EmailField()
    seller_description = models.TextField(blank=True,null=False)
    is_verified = models.BooleanField(default=False)


    def get_logo_url(self):
        logo = self.logoImages.first()
        if logo:
            return f"{logo.mongo_filename}"
        return None

    def save(self, *args, **kwargs):
        if not self.user.is_seller:
            self.user.is_seller = True
            self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user.username})"

class LogoImage(models.Model):
    logo = models.ForeignKey('Seller', on_delete=models.CASCADE, related_name='logoImages',null=False,blank=False)
    mongo_filename = models.CharField(max_length=255)

    def __str__(self):
        return f"MongoDB Image for {self.logo}: {self.mongo_filename}"
    

@receiver(post_delete, sender=Seller)
def delete_images_for_sellers_logos(sender, instance, **kwargs):
    try:
        files = fs.find({'metadata.seller_logo_uid': str(instance.uid)})
        for file in files:
            fs.delete(file._id)
    except Exception as e:
        print(f"Error deleting logos for seller {instance.id}: {e}")


class Locations(Common):
    town = models.CharField(max_length=200,blank=False,null=False)
    county = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self) -> str:
        return f"{self.county}"

class Tractor(Common):
    BRANDS = (
        ('John Deere','John Deere'),
        ('Massey Ferguson','Massey Ferguson'),
        ('Mahindra','Mahindra'),
        ('Swaraj','Swaraj')
    )
    CONDITION = (
        ('New Tractor','New Tractor'),
        ('Used Tractor','Used Tractor'),
    )

    TRANSMISSION = (('Automatic','Automatic'),
                    ('Manual','Manual'),
                    ('Electric','Electric'),
                    )

    FUEL_TYPE = (('Diesel','Diesel'),
                 ('Petrol','Petrol'))
    tractor_seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="tractors")
    tractor_name = models.CharField(max_length=250, blank=False, null=False)
    model = models.CharField(max_length=30, blank=False, null=False, choices=BRANDS, default='John Deere')
    year_of_manufucture = models.CharField(max_length=10, blank=False, null=False)
    engine_capacity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    location = models.CharField(max_length=20, blank=False, null=False, choices=(
        ('Nairobi','Nairobi'),
        ('Kisumu','Kisumu'),
        ('Mombasa','Mombasa')
    ), default='Nairobi')
    condition = models.CharField(max_length=30, blank=False, null=False, choices=CONDITION, default='Old')
    fuel_type = models.CharField(max_length=30, blank=False, null=False, choices=FUEL_TYPE, default='Petrol')
    transmission = models.CharField(max_length=10, blank=False, null=False, choices=TRANSMISSION, default='Manual')
    Tractor_description = models.TextField()
    Wheel_Drive = models.CharField(max_length=30, blank=False, null=False)
    horse_power = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    Number_of_cylinders = models.PositiveIntegerField(default=0)
    mileage = models.DecimalField(max_digits=20,decimal_places=2,default=0)
    forward_speed = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    reverse_speed = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    lifting_capacity = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    is_featured = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.tractor_name} - {self.model} ({self.year_of_manufucture})"
    
    def save(self, *args, **kwargs):
        # Check if tractor_seller is not explicitly set
        if not self.tractor_seller and 'request' in kwargs:
            request = kwargs.pop('request')
            if hasattr(request.user, 'is_seller'):  
                self.tractor_seller = request.user.seller_profile
        super().save(*args, **kwargs)
    


class TractorImage(models.Model):
    tractor = models.ForeignKey('Tractor', on_delete=models.CASCADE, related_name='images')
    mongo_filename = models.CharField(max_length=255) 

    def __str__(self):
        return f"Image for {self.tractor.tractor_name}: {self.mongo_filename}"

    

@receiver(post_delete, sender=Tractor)
def delete_images_for_tractor(sender, instance, **kwargs):
    # Delete all images associated with the tractor in MongoDB
    files = fs.find({'metadata.tractor_uid': str(instance.uid)})
    for file in files:
        fs.delete(file._id)


class Dealers(Common):
    pass


class Sellers_Emails(Common):
    customer_name = models.CharField(max_length=50)
    email = models.EmailField(blank=False,null=False)
    customer_message = models.TextField(blank=False,null=False)

    def __str__(self) -> str:
        return f"{self.customer_name}"