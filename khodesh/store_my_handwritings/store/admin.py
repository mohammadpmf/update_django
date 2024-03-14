from typing import Any
from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode
from django.contrib import messages

from .models import *

class InventoryFilter(admin.SimpleListFilter):
    LESS_THAN_3 = '<3'
    BETWEEN_3_and_10 = '<3'
    MORE_THAN_10 = '>10'
    title = 'Critical Inventory Status'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            (InventoryFilter.LESS_THAN_3, 'High'),
            (InventoryFilter.BETWEEN_3_and_10, 'Medium'),
            (InventoryFilter.MORE_THAN_10, 'OK'),
        ]
    
    def queryset(self, request, queryset):
        if self.value() == InventoryFilter.LESS_THAN_3:
            return queryset.filter(inventory__lt=3)
        if self.value() == InventoryFilter.BETWEEN_3_and_10:
            return queryset.filter(inventory__range=(3, 10))
        if self.value() == InventoryFilter.MORE_THAN_10:
            return queryset.filter(inventory__gt=10)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'inventory', 'unit_price', 'inventory_status', 'category_title', 'number_of_comments']
    list_display_links = ['id', 'name', 'inventory']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['category']
    ordering = ['-id']
    list_filter = ['datetime_created', 'unit_price', 'category', InventoryFilter]
    actions = ['clear_inventory']
    search_fields = ['name', ]
    autocomplete_fields = ['category']
    prepopulated_fields = {
        'slug': ['name', ]
    }
    # fields = ['name', 'slug']
    # exclude = ['discounts']
    readonly_fields = ['category']

    def inventory_status(self, product: Product):
        temp = product.inventory
        if temp<10:
            return "Low"
        elif temp<50:
            return "Medium"
        return "High"

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('comments').annotate(comments_count=Count('comments'))
    
    @admin.display(description="تعداد کامنت ها", ordering='comments_count')
    def number_of_comments(self, product: Product):
        # return product.comments_count
        url = (
            reverse('admin:store_comment_changelist')
            + '?'
            + urlencode({
                'product__id': product.id
            })
        )
        return format_html(f'<a href="{url}">{product.comments_count}</a>')
    
    @admin.display(ordering='category__title')
    def category_title(self, product: Product):
        return product.category.title
    
    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset):
        result = queryset.update(inventory=0)
        self.message_user(request, f"{result} تعداد از اینونتوری ها با موفقیت ۰ شدند. :D", messages.ERROR)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['product', 'quantity', 'unit_price']
    extra = 0
    min_num=1
    max_num=10

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'customer','datetime_created', 'num_of_items']
    list_editable = ['status']
    list_per_page = 10
    ordering = ['datetime_created']
    inlines = [OrderItemInline]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('items').annotate(items_count=Count('items'))
    
    @admin.display(ordering='items_count', description='تعداد اقلام')
    def num_of_items(self, order:Order):
        return order.items_count
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'product']
    list_per_page = 10
    list_editable = ['status']
    autocomplete_fields = ['product', ]

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', ]
    list_per_page = 10
    ordering = ['last_name', 'first_name', ]
    search_fields = ['last_name__istartswith', 'first_name__istartswith', ]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order','product','quantity','unit_price',
]
    autocomplete_fields = ['product']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['title']


admin.site.register(Discount)
admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(CartItem)
