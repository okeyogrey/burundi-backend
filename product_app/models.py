from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    def __str__(self):
        return self.name

# NEW: A “Size” model that also belongs to a main Category
class Size(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    def __str__(self):
        return self.name

# UPDATED: Brand now references Category
class Brand(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(default="No description available")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True)

    # UPDATED: brand references the new Brand model
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)

    # NEW: sizes ManyToMany
    sizes = models.ManyToManyField(Size, blank=True)

    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', default='default_image.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    is_on_sale = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# The rest of your code, e.g. Review, etc.
class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}/5)"
