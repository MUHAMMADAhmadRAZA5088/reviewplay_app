from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse  # Import reverse
from django.utils.html import format_html  # Import format_html
from django.utils.html import mark_safe
from .models import CategoryUsers, Businessdetail, Employee, Product, ProductImage, Barcode, UserDetail, Feedback

from django.contrib import admin
# from .models import CategoryUsers, Employee, Product, UploadedImages
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
    list_display = ('business', 'business_name', 'category', 'sub_category', 'abn_number','delete_option')

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
    list_display = ('product', 'image')

@admin.register(Barcode)
class BarcodeAdmin(admin.ModelAdmin):
    list_display = ('product', 'barcode_value')

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

admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(UserDetail, UserDetailAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Employee,EmployeeAdmin)
admin.site.register(Businessdetail, BusinessdetailAdmin)
admin.site.register(CategoryUsers, CategoryUsersAdmin)







