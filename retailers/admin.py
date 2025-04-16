from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Retailer

@admin.register(Retailer)
class RetailerAdmin(UserAdmin):
    # Fields to display in the list view
    list_display = ['username', 'email', 'store_name', 'business_name', 'phone_number', 'is_verified', 'is_staff', 'is_active']
    
    # Add filtering options
    list_filter = ['is_verified', 'is_staff', 'is_active', 'date_joined']
    
    # Add search capability
    search_fields = ['username', 'email', 'store_name', 'business_name', 'phone_number']
    
    # Organize fields into fieldsets for better organization
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Business Details', {
            'fields': ('store_name', 'business_name', 'phone_number', 'address'),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Separate fieldsets for adding a new retailer
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
        ('Business Details', {
            'classes': ('wide',),
            'fields': ('store_name', 'business_name', 'phone_number', 'address'),
        }),
        ('Permissions', {
            'classes': ('collapse',),
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified'),
        }),
    )
    
    # Add ability to filter retailers in admin list by username letter
    list_filter = ['is_verified', 'is_staff', 'is_active', 'date_joined']
    
    # Order retailers by username by default
    ordering = ['username']
