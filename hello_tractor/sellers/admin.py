from django.contrib import admin

from django.contrib import admin

from sellers.forms import TractorImageForm
from .models import Seller, Tractor, TractorImage


class TractorImageInline(admin.TabularInline):
    model = TractorImage
    extra = 1  # Number of additional image fields
    form = TractorImageForm

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'is_verified')
    search_fields = ('first_name', 'last_name', 'user__username')

@admin.register(Tractor)
class TractorAdmin(admin.ModelAdmin):
    list_display = ('tractor_name', 'model', 'price', 'location', 'condition', 'is_available')
    list_filter = ('model', 'location', 'condition', 'is_available')
    search_fields = ('tractor_name', 'model', 'tractor_seller__user__username')
    inlines = [TractorImageInline]

