# models.py
from django.db import models
from django.conf import settings
from product_app.models import Product

class Order(models.Model):
    PICKUP_LOCATIONS = [
        ('CBD', 'Nairobi CBD'),
        ('WESTLANDS', 'Westlands'),
        ('KAREN', 'Karen'),
        ('THIKA', 'Thika Road'),
        ('KITENGELA', 'Kitengela'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True)
    mpesa_transaction_id = models.CharField(max_length=50, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('shipped', 'Shipped'),
            ('delivered', 'Delivery In Progress'),
        ],
        default='pending'
    )
    tracking_code = models.CharField(max_length=100, blank=True)
    pickup_location = models.CharField(
        max_length=100,
        choices=PICKUP_LOCATIONS,
        blank=True,
        help_text="Customer-selected pickup point."
    )

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"OrderItem {self.id}"

    def get_cost(self):
        return self.price * self.quantity
