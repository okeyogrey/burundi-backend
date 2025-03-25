from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    """
    Subcategory that belongs to a main Category.
    Now has related_name='subcategories' so we can do main_cat.subcategories.all().
    """
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'  # <--- ADDED
    )

    def __str__(self):
        if self.category:
            return f"{self.category.name} > {self.name}"
        return self.name

class SubSubcategory(models.Model):
    """
    SubSubcategory that belongs to a Subcategory (third level).
    We add related_name='sub_subcategories' for easy looping: subcat.sub_subcategories.all().
    """
    name = models.CharField(max_length=100)
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sub_subcategories'  # <--- ADDED
    )

    def __str__(self):
        if self.subcategory:
            return f"{self.subcategory} > {self.name}"
        return self.name

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

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(default="No description available")
    price = models.DecimalField(max_digits=10, decimal_places=2)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True)
    sub_subcategory = models.ForeignKey(SubSubcategory, on_delete=models.SET_NULL, null=True, blank=True)

    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    sizes = models.ManyToManyField(Size, blank=True)

    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', default='default_image.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    is_on_sale = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            total = sum(r.rating for r in reviews)
            return round(total / reviews.count(), 1)
        return 0

class Review(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='reviews',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}/5)"
