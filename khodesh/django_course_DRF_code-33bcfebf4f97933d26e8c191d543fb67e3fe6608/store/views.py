from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Order, OrderItem, Address, Customer, Category
from .serializers import ProductSerializer, CategorySerializer, OrderSerializer, OrderItemsSerializer, AddressSerializer, CustomerSerializer


@api_view()
def product_list(request):
    queryset = Product.objects.all().select_related('category').order_by('pk')
    serializer = ProductSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def product_detail(request, pk):
    if request.method=='GET':
        product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    elif request.method=='POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data
        return Response("OK")
        # if serializer.is_valid():
        #     serializer.validated_data
        #     return Response("OK")
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)

@api_view()
def addresses_list(request):
    queryset = Address.objects.all().select_related('customer')
    serializer = AddressSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view()
def customers_list(request):
    queryset = Customer.objects.all().select_related('address')
    serializer = CustomerSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view()
def orders_list(request):
    queryset = Order.objects.all().select_related('customer', 'customer__address')
    serializer = OrderSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view()
def order_items_list(request):
    # queryset = OrderItem.objects.all().select_related("order__customer__address", "product__category") 
    # in ham faghat 1 doone query mizaneh. amma payinia ro neveshtam chon az oon be in residam va vazehtar bayan shodeh.
    # Ama in ham chon too masire akhari ke dare mire vasati ha ro ham mibine, khodesh oona ro ham migire va jaleb hast.
    queryset = OrderItem.objects.all().select_related('order', 'order__customer', "order__customer__address", "product", "product__category")
    serializer = OrderItemsSerializer(queryset, many=True)
    return Response(serializer.data)

