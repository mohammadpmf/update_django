from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer

@api_view()
def product_list(request):
    queryset = Product.objects.all().select_related('category').order_by('pk')
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view()
def product_detail(request, pk):
    product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view()
def orders_list(request):
    queryset = Order.objects.all().select_related('customer').select_related('customer__address')
    serializer = OrderSerializer(queryset, many=True)
    return Response(serializer.data)
