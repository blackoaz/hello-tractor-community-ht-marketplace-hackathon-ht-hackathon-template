from django.contrib import admin

from .models import CustomUser,NewsletterSubscription


admin.site.register(CustomUser)
admin.site.register(NewsletterSubscription)


