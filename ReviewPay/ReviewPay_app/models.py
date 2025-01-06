
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

class CategoryUsers(AbstractUser):
    # Custom fields for normal users
    ROLE_CHOICES = [
        ('user', 'User'),
        ('business', 'Business User'),
    ]
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES,default="admin user")


class Businessdetail(models.Model):
    business = models.OneToOneField(CategoryUsers, on_delete=models.CASCADE, related_name="businesses")
    businessLogo = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    sub_category = models.CharField(max_length=100, null=True, blank=True)
    abn_number = models.CharField(max_length=20, null=True, blank=True)
    business_name = models.CharField(max_length=100, null=True, blank=True)
    business_address = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Business Detail"
        verbose_name_plural = "Business Details"  # Plural form

    def __str__(self):
        return self.business_name or "Unnamed Business"


# Employee Model
class Employee(models.Model):
    business = models.ForeignKey(CategoryUsers, on_delete=models.CASCADE, related_name="employees")
    employee_name = models.CharField(max_length=255)
    identification_number = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    employee_email_address = models.EmailField()
    working_since  = models.CharField(max_length=100)
    employee_profiles = models.ImageField(upload_to='employee_profiles/', blank=True, null=True)

    class Meta:
        verbose_name = "Employee Detail"
        verbose_name_plural = "Employees Details"  # Plural Form

    

        
# Product Model
class Product(models.Model):
    business = models.ForeignKey(CategoryUsers, on_delete=models.CASCADE, related_name="products")
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()
    product_price = models.CharField(max_length=255)
    product_images = models.ImageField(upload_to='product_images/', blank=True, null=True)

    class Meta:
        verbose_name = "Products Details"
        verbose_name_plural = "Products Details"  # Plural Form

    def __str__(self):
        return self.business_name or "Unnamed Business"

class UserDetail(models.Model):
    business = models.OneToOneField(CategoryUsers, on_delete=models.CASCADE, related_name="user")
    first_name = models.CharField(max_length=255)
    last_name = models.TextField()
    gender = models.CharField(max_length=255)
    date_of_birth  = models.DateField()
    profile_image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    class Meta:
        verbose_name = "User Detail"
        verbose_name_plural = "User Details"  # Plural Form

    def __str__(self):
        return self.first_name or "Unnamed Business"

# # UploadedImages Model
# class UploadedImages(models.Model):
#     business = models.ForeignKey(CategoryUsers, on_delete=models.CASCADE, related_name="uploaded_images")
#     business_images = models.ImageField(upload_to='business_images/')






