from django.contrib import admin
from .models import Order, OrderItem, Product, Category, Brand


admin.site.register(Category) 
admin.site.register(Brand) 
admin.site.register(Order)
admin.site.register(OrderItem)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'brand')  # Shows name, price, category, and brand in the admin panel
