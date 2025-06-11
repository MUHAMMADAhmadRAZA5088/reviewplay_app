from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse  # Import reverse
from django.utils.html import format_html  # Import format_html
from django.utils.html import mark_safe
from .models import CategoryUsers, Businessdetail, Employee, Product,Product_business_invoice
from .models import BusinessState, ProductImage, Barcode, UserDetail, favorate_business
from .models import Feedback, BusinessVerifications,CommingsoonLogin,Welcome_new_user
from .models import BusinessLogo,BusinessVideo,BusinessImage,ReviewCashback,Notifications
from .models import ReferralCashback,ReferralCashback, UserCashBack, OrderTracking,QRScan
from .models import Follow, ProductClientReview, UserSession
#BusinessImage, BusinessVideo
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Custom User Admin
class CategoryUsersAdmin(UserAdmin):
    model = CategoryUsers

    # Fields to display in list view
    list_display = ('id','name', 'referral_code' ,'email', 'role', 'delete_option')

    # Fields to filter
    list_filter = ('role',)
  
    # Custom column for delete
    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
             '<button class="admin_btn-primary"><a style="text-decoration: none;color: #fff;" href="{}">Delete</a></button>',
            delete_url
        )
        class Media:
            css = {
                'all': ('css/custom.css',)  # Ensure correct static path
            }   

    delete_option.short_description = 'Delete'  # Column header name
 
# Register the Businessdetail model with its own admin class
class BusinessdetailAdmin(admin.ModelAdmin):
    list_display = ('id','business','marchant_api_key' ,'business_name', 'category', 'sub_category', 'abn_number', 'created_at' ,'delete_option')

   
        # Custom column for delete
    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
             '<button class="admin_btn-primary"><a style="text-decoration: none;color: #fff;" href="{}">Delete</a></button>',
            delete_url
        )
        class Media:
            css = {
                'all': ('css/custom.css',)  # Ensure correct static path
            }
class BusinessLogoAdmin(admin.ModelAdmin):
    list_display = ('id','business', 'image', 'delete_option')

    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
             '<button class="admin_btn-primary"><a style="text-decoration: none;color: #fff;" href="{}">Delete</a></button>',
            delete_url
        )
        class Media:
            css = {
                'all': ('css/custom.css',)  # Ensure correct static path
            }

# Register the Employee model with its own admin class
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id','business', 'employee_name', 'identification_number', 'designation','working_since', 'employee_email_address','delete_option')

        # Custom column for delete
    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
             '<button class="admin_btn-primary"><a style="text-decoration: none;color: #fff;" href="{}">Delete</a></button>',
            delete_url
        )
    class Media:
        css = {
            'all': ('css/custom.css',)  # Ensure correct static path
        }

# Register the Products model with its own admin class
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','business', 'product_name', 'product_description', 'product_price','delete_option')

        # Custom column for delete
    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
             '<button class="admin_btn-primary"><a style="text-decoration: none;color: #fff;" href="{}">Delete</a></button>',
            delete_url
        )
         
    class Media:
            css = {
                'all': ('css/custom.css',)  # Ensure correct static path
            }

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id','product', 'image', 'delete_option')

    def delete_option(self, obj):

        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
             '<button class="admin_btn-primary"><a style="text-decoration: none;color: #fff;" href="{}">Delete</a></button>',
            delete_url
        )
        class Media:
            css = {
                'all': ('css/custom.css',)  # Ensure correct static path
            }



@admin.register(Barcode)
class BarcodeAdmin(admin.ModelAdmin):
    list_display = ('id','product', 'barcode_value', 'delete_option')

    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
             '<button class="admin_btn-primary"><a style="text-decoration: none;color: #fff;" href="{}">Delete</a></button>',
            delete_url
        )

    class Media:
        css = {
            'all': ('css/custom.css',)  # Ensure correct static path
        }
@admin.register(BusinessVerifications)
class BusinessVerificationsAdmin(admin.ModelAdmin):
    list_display = ('id','business', 'ACN', 'business_web','fullname_director_1' , 'fullname_director_2', 'admin_phone_number', 'business_phone_number','facebook_link' , 'instra_link', 'admin_email','client_email' , 'openning_hours', 'government_issue_document', 'business_name_evidence','company_extract_issue' ,'delete_option')

    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
             '<button class="admin_btn-primary"><a style="text-decoration: none;color: #fff;" href="{}">Delete</a></button>',
            delete_url
        )
                   
        class Media:
            css = {
                'all': ('css/custom.css',)  # Ensure correct static path
            }

class UserDetailAdmin(admin.ModelAdmin):
    list_display = ('id','business', 'first_name', 'last_name', 'gender','date_of_birth','email','phone_number','post_code','profile_image','delete_option')

        # Custom column for delete
    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
             '<button class="admin_btn-primary"><a style="text-decoration: none;color: #fff;" href="{}">Delete</a></button>',
            delete_url
        )
        class Media:
            css = {
                'all': ('css/custom.css',)  # Ensure correct static path
            }
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'business', 'issue_category', 'issue_description','urgency_level')

        # Custom column for delete
    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
             '<button class="admin_btn-primary"><a style="text-decoration: none;color: #fff;" href="{}">Delete</a></button>',
            delete_url
        )
        class Media:
            css = {
                'all': ('css/custom.css',)  # Ensure correct static path
            }

class BusinessStateAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'product_name',  # Product name
        'quality',       # Editable field
        'quality_progress_bar', 
        'performance',   # Editable field
        'performance_progress_bar', 
        'easy_to_use',   # Editable field
        'easy_to_use_progress_bar', 
        'durability',    # Editable field
        'durability_progress_bar', 
    )
    list_editable = ('quality', 'performance', 'easy_to_use', 'durability')  # Editable fields

    # Quality Progress Bar
    def quality_progress_bar(self, obj):
        return self._generate_progress_bar(obj.quality)
    quality_progress_bar.short_description = 'Quality Progress'

    # Performance Progress Bar
    def performance_progress_bar(self, obj):
        return self._generate_progress_bar(obj.performance)
    performance_progress_bar.short_description = 'Performance Progress'

    # Easy to Use Progress Bar
    def easy_to_use_progress_bar(self, obj):
        return self._generate_progress_bar(obj.easy_to_use)
    easy_to_use_progress_bar.short_description = 'Easy to Use Progress'

    # Durability Progress Bar
    def durability_progress_bar(self, obj):
        return self._generate_progress_bar(obj.durability)
    durability_progress_bar.short_description = 'Durability Progress'

    # Helper Function to Generate Progress Bar
    def _generate_progress_bar(self, value):
        return format_html(
            '<div style="width: 100%; background-color: #f3f3f3; border: 1px solid #ddd;">'
            '<div style="width: {}%; background-color: #4caf50; padding: 5px 0; color: white; text-align: center;">'
            '{}%</div></div>',
            value, value
        )


class CommingsoonLoginAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'email', 'phone_number','delete_option')

        # Custom column for delete
    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
            '<button class="admin_btn-primary"><a style="text-decoration: none;color: #fff;" href="{}">Delete</a></button>',
            delete_url
        )

        delete_option.allow_tags = True
        delete_option.short_description = "Delete"

        class Media:
            css = {
                'all': ('css/custom.css',)  # Ensure correct static path
            }

class BusinessVideoAdmin(admin.ModelAdmin):
    list_display = ('id','business', 'video','delete_option')

    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
             '<button class="admin_btn-primary"><a style="text-decoration: none;color: #fff;" href="{}">Delete</a></button>',
            delete_url
        )

        delete_option.allow_tags = True
        delete_option.short_description = "Delete"

        class Media:
            css = {
                'all': ('css/custom.css',)  # Ensure correct static path
            }

class BusinessImageAdmin(admin.ModelAdmin):
    list_display = ('id','business', 'image','delete_option')

    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
             '<button class="admin_btn-primary"><a style="text-decoration: none;color: #fff;" href="{}">Delete</a></button>',
            delete_url
        )

        delete_option.allow_tags = True
        delete_option.short_description = "Delete"

        class Media:
            css = {
                'all': ('css/custom.css',)  # Ensure correct static path
            }

class ReviewCashbackAdmin(admin.ModelAdmin):
    list_display = (
                    'id','business', 'review_amount_cashback_percent',
                    'review_amount_cashback_fixed','review_cashback_return_refund_period',
                    'review_cashback_expiry','delete_option'
                    )

    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
             '<button class="admin_btn-primary"><a style="text-decoration: none;color: #fff;" href="{}">Delete</a></button>',
            delete_url
        )

        delete_option.allow_tags = True
        delete_option.short_description = "Delete"

        class Media:
            css = {
                'all': ('css/custom.css',)  # Ensure correct static path
            }

class ReferralCashbackAdmin(admin.ModelAdmin):
    list_display = (
                    'id','business', 'referral_cashback_enabled', 'referral_amount_cashback_percent',
                    'referral_amount_cashback_fixed','referral_cashback_return_refund_period',
                    'referral_cashback_expiry','delete_option'
                    )

    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
            '<button class="admin_btn-primary"><a style="text-decoration: none;color: #fff;" href="{}">Delete</a></button>',
            delete_url
        )

        delete_option.allow_tags = True
        delete_option.short_description = "Delete"

        class Media:
            css = {
                'all': ('css/custom.css',)  # Ensure correct static path
            }

class UserCashBackAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'business_id', 'invoice_price', 'amount', 'created_date', 'delete_option'
    )


    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
            '<button class="admin_btn-primary"><a style="text-decoration: none;color: #fff;" href="{}">Delete</a></button>',
            delete_url
        )

        delete_option.allow_tags = True
        delete_option.short_description = "Delete"

        class Media:
            css = {
                'all': ('css/custom.css',)  # Ensure correct static path
            }

class OrderTrackingAdmin(admin.ModelAdmin):
    list_display = ('id','marchant_api','adv_sub' ,'adv_sub2', 'adv_sub3', 'adv_sub4', 'adv_sub5',
    'transaction_id','amount','user_id','status','delete_option')

        # Custom column for delete
    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
             '<button class="admin_btn-primary"><a style="text-decoration: none;color: #fff;" href="{}">Delete</a></button>',
            delete_url
        )
        class Media:
            css = {
                'all': ('css/custom.css',)  # Ensure correct static path
            }

class QRScanAdmin(admin.ModelAdmin):
    list_display = ('id','user_id','business_id','scan_url','status','scanned_at','delete_option')
    # Custom column for delete
    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
             '<button class="admin_btn-primary"><a style="text-decoration: none;color: #fff;" href="{}">Delete</a></button>',
            delete_url
        )
        class Media:
            css = {
                'all': ('css/custom.css',)  # Ensure correct static path
            }

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id','user_id','business_detail','business_detail_date','product_image','product_image_date','business_verify','business_verify_date','delete_option')
    # Custom column for delete
    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
             '<button class="admin_btn-primary"><a style="text-decoration: none;color: #fff;" href="{}">Delete</a></button>',
            delete_url
        )
        class Media:
            css = {
                'all': ('css/custom.css',)  # Ensure correct static path
            }
class Welcome_new_userAdmin(admin.ModelAdmin):
    list_display = ('id','email','delete_option')
    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
             '<button class="admin_btn-primary"><a style="text-decoration: none;color: #fff;" href="{}">Delete</a></button>',
            delete_url
        )
        class Media:
            css = {
                'all': ('css/custom.css',)  # Ensure correct static path
            }
class favorate_businessAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'business_id', 'delete_option')
    def user_id(self, obj):
        return obj.user.id  # Display user ID instead of name

    def business_id(self, obj):
        return obj.business.id  # Display business ID instead of name

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # This will ensure the ForeignKey fields display IDs in admin forms as well
        if db_field.name == "user":
            kwargs["queryset"] = UserDetail.objects.all()
        elif db_field.name == "business":
            kwargs["queryset"] = Businessdetail.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
             '<button class="admin_btn-primary"><a style="text-decoration: none;color: #fff;" href="{}">Delete</a></button>',
            delete_url
        )
        class Media:
            css = {
                'all': ('css/custom.css',)  # Ensure correct static path
            }
class Product_business_invoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'business_id', 'product_service', 'invoice_amount', 'reviewcashback', 'refferial_code','client_name','client_phone','client_email','proof_purchase','delete_option')
        # Custom column for delete
    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
             '<button class="admin_btn-primary"><a style="text-decoration: none;color: #fff;" href="{}">Delete</a></button>',
            delete_url
        )
        class Media:
            css = {
                'all': ('css/custom.css',)  # Ensure correct static path
            }

class ProductClientReviewAdmn(admin.ModelAdmin):
    list_display = ('id', 'product_id', 'user', 'business','benefit_quality', 'delete_option')
        # Custom column for delete
    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
             '<button class="admin_btn-primary"><a style="text-decoration: none;color: #fff;" href="{}">Delete</a></button>',
            delete_url
        )
        class Media:
            css = {
                'all': ('css/custom.css',)  # Ensure correct static path
            }

class FollowAdmn(admin.ModelAdmin):
    list_display = ('id', 'follower', 'following', 'created_at')
        # Custom column for delete
    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
             '<button class="admin_btn-primary"><a style="text-decoration: none;color: #fff;" href="{}">Delete</a></button>',
            delete_url
        )
        class Media:
            css = {
                'all': ('css/custom.css',)  # Ensure correct static path
            }

class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'duration', 'timestamp')
        # Custom column for delete
    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
             '<button class="admin_btn-primary"><a style="text-decoration: none;color: #fff;" href="{}">Delete</a></button>',
            delete_url
        )
        class Media:
            css = {
                'all': ('css/custom.css',)  # Ensure correct static path
            }

admin.site.register(UserSession ,UserSessionAdmin)
admin.site.register(ProductClientReview ,ProductClientReviewAdmn)
admin.site.register(Follow ,FollowAdmn)
admin.site.register(Product_business_invoice, Product_business_invoiceAdmin)  
admin.site.register(favorate_business, favorate_businessAdmin)   
admin.site.register(Welcome_new_user, Welcome_new_userAdmin)
admin.site.register(Notifications,NotificationAdmin)
admin.site.register(QRScan,QRScanAdmin)
admin.site.register(OrderTracking,OrderTrackingAdmin)
admin.site.register(UserCashBack,UserCashBackAdmin)
admin.site.register(ReferralCashback,ReferralCashbackAdmin)
admin.site.register(ReviewCashback,ReviewCashbackAdmin)
admin.site.register(BusinessImage,BusinessImageAdmin)
admin.site.register(BusinessVideo,BusinessVideoAdmin)
admin.site.register(BusinessLogo,BusinessLogoAdmin)
admin.site.register(CommingsoonLogin, CommingsoonLoginAdmin)
admin.site.register(BusinessState, BusinessStateAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(UserDetail, UserDetailAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Employee,EmployeeAdmin)
admin.site.register(Businessdetail, BusinessdetailAdmin)
admin.site.register(CategoryUsers, CategoryUsersAdmin)







