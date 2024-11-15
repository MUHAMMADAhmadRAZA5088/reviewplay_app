from django.contrib.auth.models import AbstractUser
from django.db import models

class CategoryUsers(AbstractUser):
    # Custom fields for normal users
    ROLE_CHOICES = [
        ('custom', 'User'),
        ('business', 'Business User'),
    ]

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES,default="admin user")
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    sub_category = models.CharField(max_length=100, null=True, blank=True)
    abn_number = models.CharField(max_length=20, null=True, blank=True)
    business_name = models.CharField(max_length=100, null=True, blank=True)
    business_address = models.TextField(null=True, blank=True)







