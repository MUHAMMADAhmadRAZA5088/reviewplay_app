
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
    businessLogo = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    sub_category = models.CharField(max_length=100, null=True, blank=True)
    abn_number = models.CharField(max_length=20, null=True, blank=True)
    business_name = models.CharField(max_length=100, null=True, blank=True)
    business_address = models.TextField(null=True, blank=True)


# Employee Model
class Employee(models.Model):
    business = models.ForeignKey(CategoryUsers, on_delete=models.CASCADE, related_name="employees")
    employee_name = models.CharField(max_length=255)
    identification_number = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    employee_email_address = models.EmailField()
    employee_profiles = models.ImageField(upload_to='employee_profiles/', blank=True, null=True)

# Product Model
class Product(models.Model):
    business = models.ForeignKey(CategoryUsers, on_delete=models.CASCADE, related_name="products")
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()
    product_price = models.CharField(max_length=255)
    product_images = models.ImageField(upload_to='product_images/', blank=True, null=True)

# UploadedImages Model
class UploadedImages(models.Model):
    business = models.ForeignKey(CategoryUsers, on_delete=models.CASCADE, related_name="uploaded_images")
    business_images = models.ImageField(upload_to='business_images/')





