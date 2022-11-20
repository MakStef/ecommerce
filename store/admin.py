from django.contrib import admin

from .models import (
    ProductSupercategory,
    ProductCategory,
    ProductSubcategory,
    Product,
)

# Register your models here.
admin.site.register(ProductSupercategory)
admin.site.register(ProductCategory)
admin.site.register(ProductSubcategory)
admin.site.register(Product)
