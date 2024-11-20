from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Common(models.Model):
    uid = models.UUIDField(default=uuid.uuid4(),primary_key=True, editable=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Seller(Common):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    # contact_number = models.PhoneNumberField()
    contact_email = models.EmailField()
    is_verified = models.BooleanField(default=False)

class Tractor(Common):
    BRANDS = (
        ('John Deere','Deere'),
        ('Mercy Ferguson','Ferguson')
    )
    CONDITION = (
        ('New','New'),
        ('Second Hand','Old'),
    )

    TRANSMISSION = (('Automatic','Automatic'),('Manual','Manual'))

    FUEL_TYPE = (('Diesel','Diesel'),
                 ('Petrol','Petrol'))
    tractor_seller = models.OneToOneField(Seller, on_delete=models.CASCADE)
    tractor_name = models.CharField(max_length=250,blank=False,null=False)
    model = models.CharField(max_length=30, blank=False,null=False, choices=BRANDS,default='John Deere')
    year_of_manufucture = models.CharField(max_length=10, blank=False,null=False)
    engine_capacity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12,decimal_places=2)
    location = models.CharField(max_length=20, blank=False,null=False,choices=(('Nairobi','Nairobi'),('Mombasa','Mombasa'),('Kisumu','Kisumu')), default='Nairobi')
    condition = models.CharField(max_length=30, blank=False,null=False, choices=CONDITION,default='Old')
    fuel_type = models.CharField(max_length=30, blank=False,null=False, choices=FUEL_TYPE,default='Petrol')
    transmission = models.CharField(max_length=10, blank=False,null=False, choices=TRANSMISSION,default='Manual')
    is_featured = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
