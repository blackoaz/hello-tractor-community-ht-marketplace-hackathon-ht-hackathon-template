import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class Common(models.Model):
    uid = models.UUIDField(default=uuid.uuid4(),primary_key=True, editable=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUser(AbstractUser):
    is_seller = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_seller = True
        super().save(*args, **kwargs)



class NewsletterSubscription(Common):
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return f"{self.email}"




