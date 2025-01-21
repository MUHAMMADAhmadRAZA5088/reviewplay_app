
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
    businessLogo = models.ImageField(upload_to='business_logo/', null=True, blank=True)
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


class BusinessVideo(models.Model):
    business = models.ForeignKey(Businessdetail, on_delete=models.CASCADE, related_name="business_video")
    video = models.FileField(upload_to='business_videos/', null=True, blank=True)

class BusinessImage(models.Model):
    business = models.ForeignKey(Businessdetail, on_delete=models.CASCADE, related_name="business_image")
    image = models.FileField(upload_to='business_images/', null=True, blank=True)

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

    class Meta:
        verbose_name = "Products Details"
        verbose_name_plural = "Products Details"  # Plural Form



class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')  # Ensure this field name is correct



class Barcode(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='barcode')  # Relation to Product
    barcode_value = models.ImageField(upload_to='barcode_images/')  # Unique barcode value
    

class UserDetail(models.Model):
    business = models.OneToOneField(CategoryUsers, on_delete=models.CASCADE, related_name="user")
    first_name = models.CharField(max_length=255)
    last_name = models.TextField()
    gender = models.CharField(max_length=255)
    date_of_birth  = models.DateField()
    profile_image = models.ImageField(upload_to='user_images/', blank=True, null=True)
    class Meta:
        verbose_name = "User Detail"
        verbose_name_plural = "User Details"  # Plural Form

    def __str__(self):
        return self.first_name or "Unnamed Business"

class Feedback(models.Model):
    business = models.ForeignKey(CategoryUsers, on_delete=models.CASCADE, related_name="verifications")
    issue_category = models.CharField(max_length=255)
    issue_description = models.TextField()
    urgency_level = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedback"  # Plural Form

class BusinessVerifications(models.Model):
    business = models.OneToOneField(CategoryUsers, on_delete=models.CASCADE, related_name="category")
    ACN = models.CharField(max_length=255)
    business_web = models.CharField(max_length=255)
    fullname_director_1 = models.CharField(max_length=255)
    fullname_director_2 = models.CharField(max_length=255)
    admin_phone_number = models.CharField(max_length=255)
    business_phone_number = models.CharField(max_length=255)
    facebook_link = models.CharField(max_length=255)
    instra_link = models.CharField(max_length=255)
    admin_email = models.CharField(max_length=255)
    client_email = models.CharField(max_length=255)
    openning_hours = models.CharField(max_length=255)
    government_issue_document = models.ImageField(upload_to=f'verification_business_government_issue_document/')
    business_name_evidence = models.ImageField(upload_to=f'verification_business_business_name_evidence')
    company_extract_issue = models.ImageField(upload_to=f'verification_business_company_extract_issue')

    class Meta:
        verbose_name = "Business Verification"
        verbose_name_plural = "Business Verifications"  # Plural Form



from django.db import models

class BusinessState(models.Model):
    product_name = models.CharField(max_length=200)
    quality = models.IntegerField(default=0)        # Progress: 0-100
    performance = models.IntegerField(default=0)    # Progress: 0-100
    easy_to_use = models.IntegerField(default=0)    # Progress: 0-100
    durability = models.IntegerField(default=0)     # Progress: 0-100

    def __str__(self):
        return self.product_name






