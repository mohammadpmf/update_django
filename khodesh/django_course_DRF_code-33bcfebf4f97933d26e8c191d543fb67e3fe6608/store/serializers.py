from rest_framework import serializers
from decimal import Decimal
from .models import Customer, Category, Product
from django.utils.text import slugify

DOLLORS_TO_RIALS = 500000
TAX=Decimal(0.09)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['id']

    alaki_field = serializers.SerializerMethodField()
    num_of_products = serializers.SerializerMethodField()

    def get_alaki_field(self, category):
        return f'alaki {category.pk} {category.title}'
    
    def get_num_of_products(self, category):
        # return category.products.count()
        return category.products_count

        
    def validate(self, data):
        if len(data['title'])<3:
            raise serializers.ValidationError("Category title length should be at least 3.")
        return data

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['pk', 'name', 'category', 'description',
                   'price', 'unit_price', 'price_after_tax', 'inventory', 'amount', 
                   'datetime_created', 'datetime_modified']
    category = CategorySerializer()
    # category_link = serializers.HyperlinkedRelatedField(
    #     queryset = Category.objects.all(),
    #     view_name='category-detail',
    #     source='category'
    # )
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    amount = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField()
    # discounts = serializers.ManyRelatedField()

    def get_price_after_tax(self, product):
        return product.unit_price * (1+TAX)
    
    def validate(self, data):
        if len(data['name'])<6:
            raise serializers.ValidationError("Product title length should be at least 6.")
        return data
    
    def create(self, validated_data):
        product = Product(**validated_data)
        product.slug = slugify(product.name)
        product.save()
        return product
    
    def update(self, instance, validated_data):
        instance.inventory = validated_data.get('inventory')
        instance.name = validated_data.get('name')
        instance.unit_price = validated_data.get('unit_price')
        instance.save()
        return instance


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
