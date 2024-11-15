from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import mark_safe
from .models import CategoryUsers


class CustomUserregister(UserAdmin):
    # Display fields in the list view
    list_display = ('name', 'email', 'first_name', 'role', 'category', 'sub_category', 'abn_number', 'business_name', 'business_address','profile_picture_display')

    def profile_picture_display(self, obj):
        if obj.profile_picture:
            return mark_safe(f'<img src="{obj.profile_picture.url}" width="50" height="50" />')
        return 'No Image'
    profile_picture_display.short_description = 'Profile Picture'  # Optional: Customize header name
    search_fields = ('name', 'email')

    # Customize the detail page (when you click on a user)
    fieldsets = (
        (None, {'fields': ('name', 'password')}),
        # ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Role and Business Info', {'fields': ('role', 'category', 'sub_category', 'abn_number', 'business_name', 'business_address','profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


    # If you want to make fields editable in the list view (optional)
    # list_editable = ('role', 'category', 'sub_category', 'business_name')                                        
   

admin.site.register(CategoryUsers, CustomUserregister)



