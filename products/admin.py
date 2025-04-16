from django.contrib import admin
from .models import Product, Catalog

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'retailer', 'created_at', 'updated_at']
    list_filter = ['retailer', 'created_at', 'stock']
    search_fields = ['name', 'description', 'retailer__username']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        ('Product Information', {
            'fields': ['name', 'description', 'price', 'stock', 'image']
        }),
        ('Retailer Information', {
            'fields': ['retailer']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]

@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ['title', 'retailer', 'uploaded_at']
    list_filter = ['retailer', 'uploaded_at']
    search_fields = ['title', 'description', 'retailer__username']
    readonly_fields = ['uploaded_at']
    fieldsets = [
        ('Catalog Information', {
            'fields': ['title', 'description', 'pdf_file']
        }),
        ('Retailer Information', {
            'fields': ['retailer']
        }),
        ('Timestamps', {
            'fields': ['uploaded_at'],
            'classes': ['collapse']
        })
    ]
