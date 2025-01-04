from django.contrib import admin
from .models import Settings, Product, Image


# Register your models here.

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    pass

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass