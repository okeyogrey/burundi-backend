from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',   # Added related_name
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',   # Added related_name
        blank=True
    )
