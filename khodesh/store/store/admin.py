from django.contrib import admin

from .models import *

admin.site.register(Category)
admin.site.register(Discount)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Comment)
admin.site.register(Cart)
admin.site.register(CartItem)
