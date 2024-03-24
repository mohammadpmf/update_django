from django.shortcuts import get_object_or_404
from django.db.models import Count

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Order, OrderItem, Address, Customer, Category
from .serializers import ProductSerializer, CategorySerializer, OrderSerializer, OrderItemsSerializer, AddressSerializer, CustomerSerializer


@api_view(['GET', 'POST'])
def product_list(request):
    if request.method=='GET':
        queryset = Product.objects.all().select_related('category').order_by('pk')
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method=='POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        # if serializer.is_valid():
        #     serializer.validated_data
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
    if request.method=='GET':
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    elif request.method=='PUT':
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method=='DELETE':
        if product.order_items.count()>0:
            return Response({'error': 'There is some order item including this product. Please remove them first'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def category_list(request):
    if request.method=='GET':
        # queryset = Category.objects.all().prefetch_related('products')
        queryset = Category.objects.all().annotate(
            products_count = Count('products')
        )
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    # category = get_object_or_404(Category, pk=pk)
    category = get_object_or_404(Category.objects.annotate(products_count = Count('products')), pk=pk)
    if request.method=='GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    elif request.method=='PUT':
        serializer = CategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method=='DELETE':
        if category.products.count()>0:
            return Response({'error': 'There is some products including this category. Please remove them first'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        serializer = CategorySerializer(category)
        category.delete()
        return Response(status.HTTP_204_NO_CONTENT)


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

