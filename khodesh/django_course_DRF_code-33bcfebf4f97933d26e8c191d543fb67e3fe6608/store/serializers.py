from rest_framework import serializers
from decimal import Decimal
from random import randint

DOLLORS_TO_RIALS = 500000
TAX=Decimal(0.09)

class CategorySerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=500)
    alaki_field = serializers.SerializerMethodField()

    def get_alaki_field(self, category):
        return randint(1, 500)


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    price_after_tax = serializers.SerializerMethodField()
    # amount = serializers.IntegerField(source='inventory')
    inventory = serializers.IntegerField()
    category = CategorySerializer()

    def get_price_after_tax(self, product):
        return product.unit_price * (1+TAX)
    