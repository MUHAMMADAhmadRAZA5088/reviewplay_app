from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse  # Import reverse
from django.utils.html import format_html  # Import format_html
from django.utils.html import mark_safe
from .models import CategoryUsers, Businessdetail, Employee, Product
from .models import BusinessState, ProductImage, Barcode, UserDetail
from .models import Feedback, BusinessVerifications,CommingsoonLogin
#BusinessImage, BusinessVideo
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Custom User Admin
class CategoryUsersAdmin(UserAdmin):
    model = CategoryUsers

    # Fields to display in list view
    list_display = ('id','name', 'email', 'role', 'delete_option')

    # Fields to filter
    list_filter = ('role',)
  
    # Custom column for delete
    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
            '<a href="{}" style="padding: 5px 10px; color: white; background-color: red; border: none; border-radius: 3px; text-decoration: none;">Delete</a>',
            delete_url
        )


    delete_option.short_description = 'Delete'  # Column header name

# Register the Businessdetail model with its own admin class
class BusinessdetailAdmin(admin.ModelAdmin):
    list_display = ('business', 'business_name', 'category', 'sub_category', 'abn_number','businessLogo','delete_option')

        # Custom column for delete
    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
            '<a href="{}" style="padding: 5px 10px; color: white; background-color: red; border: none; border-radius: 3px; text-decoration: none;">Delete</a>',
            delete_url
        )


# Register the Employee model with its own admin class
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('business', 'employee_name', 'identification_number', 'designation','working_since', 'employee_email_address','delete_option')

        # Custom column for delete
    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
            '<a href="{}" style="padding: 5px 10px; color: white; background-color: red; border: none; border-radius: 3px; text-decoration: none;">Delete</a>',
            delete_url
        )

# Register the Products model with its own admin class
class ProductAdmin(admin.ModelAdmin):
    list_display = ('business', 'product_name', 'product_description', 'product_price','delete_option')

        # Custom column for delete
    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
            '<a href="{}" style="padding: 5px 10px; color: white; background-color: red; border: none; border-radius: 3px; text-decoration: none;">Delete</a>',
            delete_url
        )

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'delete_option')

    def delete_option(self, obj):

        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
            '<a href="{}" style="padding: 5px 10px; color: white; background-color: red; border: none; border-radius: 3px; text-decoration: none;">Delete</a>',
            delete_url
        )
@admin.register(Barcode)
class BarcodeAdmin(admin.ModelAdmin):
    list_display = ('product', 'barcode_value', 'delete_option')

    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
            '<a href="{}" style="padding: 5px 10px; color: white; background-color: red; border: none; border-radius: 3px; text-decoration: none;">Delete</a>',
            delete_url
        )

@admin.register(BusinessVerifications)
class BusinessVerificationsAdmin(admin.ModelAdmin):
    list_display = ('business', 'ACN', 'delete_option')

    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
            '<a href="{}" style="padding: 5px 10px; color: white; background-color: red; border: none; border-radius: 3px; text-decoration: none;">Delete</a>',
            delete_url
        )

class UserDetailAdmin(admin.ModelAdmin):
    list_display = ('business', 'first_name', 'last_name', 'gender','date_of_birth','profile_image','delete_option')

        # Custom column for delete
    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
            '<a href="{}" style="padding: 5px 10px; color: white; background-color: red; border: none; border-radius: 3px; text-decoration: none;">Delete</a>',
            delete_url
        )

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'business', 'issue_category', 'issue_description','urgency_level')

        # Custom column for delete
    def delete_option(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
            '<a href="{}" style="padding: 5px 10px; color: white; background-color: red; border: none; border-radius: 3px; text-decoration: none;">Delete</a>',
            delete_url
        )

class BusinessStateAdmin(admin.ModelAdmin):
    list_display = (
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
admin.site.register(CommingsoonLogin, CommingsoonLoginAdmin)
admin.site.register(BusinessState, BusinessStateAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(UserDetail, UserDetailAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Employee,EmployeeAdmin)
admin.site.register(Businessdetail, BusinessdetailAdmin)
admin.site.register(CategoryUsers, CategoryUsersAdmin)







