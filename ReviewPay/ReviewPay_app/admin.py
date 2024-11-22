# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from django.utils.html import mark_safe
# from .models import CategoryUsers

from django.contrib import admin
from .models import CategoryUsers, Employee, Product, UploadedImages
from django.contrib.auth.admin import UserAdmin

# Custom User Admin
class CategoryUsersAdmin(UserAdmin):
    model = CategoryUsers

    # Fields to display in list view
    list_display = ('username', 'email', 'role', 'business_name', 'category', 'is_active', 'is_staff')

    # Fields to filter
    list_filter = ('role', 'is_staff', 'is_active', 'category')

    # Search fields
    search_fields = ('username', 'email', 'business_name', 'category')

    # Editable fields in form
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email', 'role', 'business_name', 'business_address')}),
        ('Business Info', {'fields': ('businessLogo', 'category', 'sub_category', 'abn_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )
    ordering = ('username',)


# Inline Employee Admin
class EmployeeInline(admin.TabularInline):
    model = Employee
    extra = 1  # Number of empty forms to show

# Inline Product Admin
class ProductInline(admin.TabularInline):
    model = Product
    extra = 1

# Inline Uploaded Images Admin
class UploadedImagesInline(admin.TabularInline):
    model = UploadedImages
    extra = 1

# Combine Everything in CategoryUsersAdmin
class CustomCategoryUsersAdmin(CategoryUsersAdmin):
    inlines = [EmployeeInline, ProductInline, UploadedImagesInline]

# Register Models
admin.site.register(CategoryUsers, CustomCategoryUsersAdmin)
admin.site.register(Employee)
admin.site.register(Product)
admin.site.register(UploadedImages)

# class CustomUserregister(UserAdmin):
#     # Display fields in the list view
#     list_display = ('name', 'email', 'first_name', 'role', 'category', 'sub_category', 'abn_number', 'business_name', 'business_address','profile_picture_display')

#     def profile_picture_display(self, obj):
#         if obj.profile_picture:
#             return mark_safe(f'<img src="{obj.profile_picture.url}" width="50" height="50" />')
#         return 'No Image'
#     profile_picture_display.short_description = 'Profile Picture'  # Optional: Customize header name
#     search_fields = ('name', 'email')

#     # Customize the detail page (when you click on a user)
#     fieldsets = (
#         (None, {'fields': ('name', 'password')}),
#         # ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
#         ('Role and Business Info', {'fields': ('role', 'category', 'sub_category', 'abn_number', 'business_name', 'business_address','profile_picture')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )


#     # If you want to make fields editable in the list view (optional)
#     # list_editable = ('role', 'category', 'sub_category', 'business_name')                                        
   

# admin.site.register(CategoryUsers, CustomUserregister)



