from django.contrib import admin
from .models import Product

@admin.register(Product)  # This is the correct method
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'image_display']
    
    def image_display(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50"/>'
        return "No Image"

    image_display.allow_tags = True
    image_display.short_description = 'Image'
