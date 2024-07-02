
# products/admin.py
from django.contrib import admin
from .models import Product, ProductType, SkinConcern, SkinType

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_in_stock')
    search_fields = ('name', 'description')
    list_filter = ('product_types', 'skin_concerns', 'skin_types')

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType)
admin.site.register(SkinConcern)
admin.site.register(SkinType)
