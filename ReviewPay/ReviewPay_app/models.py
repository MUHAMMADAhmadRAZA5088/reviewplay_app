import secrets
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


class OrderTracking(models.Model):
    marchant_api = models.CharField(max_length=100)
    adv_sub = models.CharField(max_length=100)  # Order ID
    adv_sub2 = models.CharField(max_length=100, blank=True, null=True)  # Product Category
    adv_sub3 = models.PositiveIntegerField(blank=True, null=True)  # Product Quantity
    adv_sub4 = models.CharField(max_length=100, blank=True, null=True)  # Product ID/SKU ID
    adv_sub5 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Order Total Amount Paid
    transaction_id = models.CharField(max_length=30 )  # Unique Transaction ID
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Subtotal
    user_id = models.CharField(max_length=100)  # ReviewPay User ID
    status = models.CharField(max_length=20, default="Pending")  # Order Status
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.adv_sub} - {self.status}"


class Businessdetail(models.Model):
    marchant_api_key = models.CharField(max_length=100, unique=True, blank=True)  
    business = models.OneToOneField(CategoryUsers, on_delete=models.CASCADE, related_name="businesses")
    category = models.CharField(max_length=100, null=True, blank=True)
    sub_category = models.CharField(max_length=100, null=True, blank=True)
    abn_number = models.CharField(max_length=20, null=True, blank=True)
    business_name = models.CharField(max_length=100, null=True, blank=True)
    business_address = models.TextField(null=True, blank=True)
    business_url = models.URLField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.marchant_api_key:  # Agar API key nahi hai to generate karo
            self.marchant_api_key = secrets.token_urlsafe(32)  # 32-character long secure key
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Business Detail"
        verbose_name_plural = "Business Details"  # Plural form

    def __str__(self):
        return self.business_name or "Unnamed Business"


class BusinessVideo(models.Model):
    business = models.ForeignKey(Businessdetail, on_delete=models.CASCADE, related_name="business_video")
    video = models.FileField(upload_to='business_videos/', null=True, blank=True)

class BusinessLogo(models.Model):
    business = models.ForeignKey(Businessdetail, on_delete=models.CASCADE, related_name="business_logo")
    image = models.FileField(upload_to='business_logo//', null=True, blank=True)

class BusinessImage(models.Model):
    business = models.ForeignKey(Businessdetail, on_delete=models.CASCADE, related_name="business_image")
    image = models.FileField(upload_to='business_images/', null=True, blank=True)



# Model for Review Cashback Settings
class ReviewCashback(models.Model):
    business = models.ForeignKey(Businessdetail, on_delete=models.CASCADE, related_name="ReviewCashback")
    review_amount_cashback_percent = models.IntegerField(
        choices=[(i, f'{i}%') for i in range(1, 21)], default=1, verbose_name="Review Amount Cashback %"
    )
    review_amount_cashback_fixed = models.IntegerField(
        choices=[(i, f'{i}') for i in range(1, 51)], default=1, verbose_name="Review Amount Cashback Fixed"
    )
    review_cashback_return_refund_period = models.IntegerField(
        choices=[(i, f'{i}') for i in range(1, 61)], default=1, verbose_name="Review Cashback Return and Refund Period"
    )
    review_cashback_expiry = models.CharField(
        max_length=10, choices=[('3 months', '3 months'), ('6 months', '6 months'), ('9 months', '9 months'), ('12 months', '12 months')],
        default='3 months', verbose_name="Review Cashback Expiry"
    )

    def __str__(self):
        return f"Review Cashback Settings - {self.review_amount_cashback_percent}%"

    class Meta:
        verbose_name = "Review Cashback Setting"
        verbose_name_plural = "Review Cashback Settings"


class ReferralCashback(models.Model):
    business = models.ForeignKey(Businessdetail, on_delete=models.CASCADE, related_name="ReferralCashback")
    referral_cashback_enabled = models.BooleanField(default=False, verbose_name="Referral Cashback Enabled")
    referral_amount_cashback_percent = models.IntegerField(
        choices=[(i, f'{i}%') for i in range(1, 21)], default=1, verbose_name="Referral Amount Cashback %"
    )
    referral_amount_cashback_fixed = models.IntegerField(
        choices=[(i, f'${i}') for i in range(1, 2001)], default=1, verbose_name="Referral Amount Cashback Fixed"
    )
    referral_cashback_return_refund_period = models.IntegerField(
        choices=[(i, f'{i} days') for i in range(1, 61)], default=1, verbose_name="Referral Cashback Return and Refund Period"
    )
    referral_cashback_expiry = models.CharField(
        max_length=10, choices=[('3 months', '3 months'), ('6 months', '6 months'), ('9 months', '9 months'), ('12 months', '12 months')],
        default='3 months', verbose_name="Referral Cashback Expiry"
    )

    def __str__(self):
        return f"Referral Cashback Settings - {self.referral_amount_cashback_percent}%"

    class Meta:
        verbose_name = "Referral Cashback Setting"
        verbose_name_plural = "Referral Cashback Settings"


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


class CommingsoonLogin(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(default=0)    
    phone_number = models.CharField(max_length=15)  

    class Meta:
        verbose_name = "CommingsoonLogin"
        verbose_name_plural = "CommingsoonLogin"  # Plural Form

class UserCashBack(models.Model):
    user =  models.ForeignKey(UserDetail, on_delete=models.CASCADE, related_name="usercashback")
    business_id = models.IntegerField()
    invoice_price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.id} - User {self.user_id}"


class QRScan(models.Model):
    user_id = models.CharField(max_length=100)
    business_id = models.CharField(max_length=100)
    scan_url = models.URLField()
    status = models.CharField(max_length=20, default='pending')
    scanned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Scan by User {self.user_id} for Business {self.business_id}"


class Notifications(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('delay', 'Delay'),
    ]
    user_id = models.ForeignKey(CategoryUsers, on_delete=models.CASCADE, related_name="notifications")
    business_detail = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    business_detail_date = models.DateField(null=True, blank=True)
    product_image = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    product_image_date = models.DateField(null=True, blank=True)
    business_verify = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    business_verify_date = models.DateField(null=True, blank=True)