from django.contrib import admin
from .models import TractorBrand

# Register your models here.
@admin.register(TractorBrand)
class TractorBrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
