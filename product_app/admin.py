from django.contrib import admin
from .models import (
    Category,
    Subcategory,
    SubSubcategory,
    Brand,
    Size,
    Product,
    Review
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name']

# NEW: A separate admin page for sub-subcategories
@admin.register(SubSubcategory)
class SubSubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'subcategory']
    list_filter = ['subcategory__category']  # filter by the main Category indirectly
    search_fields = ['name']

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'category',
        'subcategory',
        'sub_subcategory',  # only if you added this field
        'brand',
        'stock',
        'image',
        'average_rating'
    ]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
