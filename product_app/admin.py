from django.contrib import admin
from .models import (
    Category,
    Subcategory,
    Brand,
    Size,       # <-- Make sure we import Size
    Product,
    Review
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']

# NEW: Register the Size model so you can add/edit sizes in admin
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']  # show these columns in admin list

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'category',
        'subcategory',
        'brand',
        'stock',
        'image',
        'average_rating'  # ensure "average_rating" is a valid method on Product
    ]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
