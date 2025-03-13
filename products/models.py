from django.db import models

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

# Brand Model
class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Product Model
class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')
    is_featured = models.BooleanField(default=False)
    is_on_sale = models.BooleanField(default=False)

    def __str__(self):
        return self.name
