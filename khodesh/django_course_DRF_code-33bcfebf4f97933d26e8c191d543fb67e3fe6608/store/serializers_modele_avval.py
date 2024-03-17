from rest_framework import serializers
from decimal import Decimal
from .models import Customer, Category

DOLLORS_TO_RIALS = 500000
TAX=Decimal(0.09)

class CategorySerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=500)
    alaki_field = serializers.SerializerMethodField()

    def get_alaki_field(self, category):
        return f'alaki {category.pk}'
    

class ProductSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    category = CategorySerializer()
    category_link = serializers.HyperlinkedRelatedField(
        queryset = Category.objects.all(),
        view_name='category-detail',
        source='category'
    )
    slug = serializers.SlugField()
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    price_after_tax = serializers.SerializerMethodField()
    inventory = serializers.IntegerField()
    amount = serializers.IntegerField(source='inventory')
    datetime_created = serializers.DateTimeField()
    datetime_modified = serializers.DateTimeField()
    # discounts = serializers.ManyRelatedField()

    def get_price_after_tax(self, product):
        return product.unit_price * (1+TAX)
    

class AddressSerializer(serializers.Serializer):
    customer = serializers.StringRelatedField()
    province = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=255)
    street = serializers.CharField(max_length=255)

class CustomerSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=255)
    birth_date = serializers.DateField()
    # address = serializers.StringRelatedField()
    address = AddressSerializer()


class OrderSerializer(serializers.Serializer):
    # customer = serializers.PrimaryKeyRelatedField(
    #     queryset = Customer.objects.all()
    # )
    # customer = serializers.StringRelatedField()
    customer = CustomerSerializer()
    datetime_created = serializers.DateTimeField()
    status = serializers.CharField(max_length=1)


class OrderItemsSerializer(serializers.Serializer):
    order = OrderSerializer()
    product = ProductSerializer()
    quantity = serializers.IntegerField()
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    total_price_of_this_order_item = serializers.SerializerMethodField()

    def get_total_price_of_this_order_item(self, order_item):
        return order_item.quantity * order_item.unit_price
