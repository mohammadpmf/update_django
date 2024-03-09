from django.contrib import admin

from .models import *

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'inventory', 'unit_price', 'inventory_status']
    list_display_links = ['id', 'name', 'inventory']
    list_editable = ['unit_price']
    list_per_page = 10

    def inventory_status(self, product: Product):
        temp = product.inventory
        if temp<10:
            return "Low"
        elif temp<50:
            return "Medium"
        return "High"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'customer','datetime_created']
    list_editable = ['status']
    list_per_page = 10
    ordering = ['datetime_created']

admin.site.register(Category)
admin.site.register(Discount)
# admin.site.register(Product, ProductAdmin)
admin.site.register(Customer)
admin.site.register(Address)
# admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Comment)
admin.site.register(Cart)
admin.site.register(CartItem)
