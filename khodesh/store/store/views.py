from django.shortcuts import render

from .models import Product, Customer, OrderItem, Order

def show_data(request):
    products = Product.objects.filter(datetime_created__year=2023)
    print(len(products))
    context = {
        'products': products
    }
    customers = Customer.objects.filter(birth_date__isnull=True)
    context['customers']=customers
    return render(request, 'welcome.html', context)

    # q = OrderItem.objects.filter(product__id=1047)
    # q = OrderItem.objects.filter(product_id=1047)
    # print(q)
    # q = Product.objects.filter(inventory=5)
    # print(q)
    # q = Product.objects.filter(name__icontains='site', inventory__gt=3)
    # print(q)
    # q = Product.objects.filter(name__icontains='site', inventory__gt=3, inventory__lt=10)
    # print(q)
    # q = Product.objects.filter(name__icontains='site', inventory__range=(3, 10))
    # print(q)
    # q = Order.objects.filter(status=Order.ORDER_STATUS_UNPAID)
    # print(q)
    # q = Order.objects.exclude(status=Order.ORDER_STATUS_UNPAID)
    # print(q)
    # q = OrderItem.objects.filter(order__id=31)
    # print(q)
    # q = OrderItem.objects.filter(order__id__range=(30, 35)).exclude(quantity__gt=10)
    # print(q)
    # q = Product.objects.filter(unit_price__lt=10)
    # print([x.unit_price for x in list(q)])

    q = OrderItem.objects.filter(order__customer__first_name__icontains="n")
    print(len(q))
    context={'q': q}
    # q_1 = Customer.objects.filter(first_name__icontains='n')
    # q_2 = OrderItem.objects.filter(order__customer__in=q_1)
    # print(len(q_2))
    return render(request, 'welcome.html', context)