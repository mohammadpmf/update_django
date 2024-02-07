from django.shortcuts import render
from django.db.models import Q, F
from django.db.models import Count, Avg, Sum, Min, Max

from .models import Product, Customer, OrderItem, Order, Comment

def show_data(request):
    # products = Product.objects.filter(Q(inventory__lt=2) | Q(inventory__gt=98))
    # products = Product.objects.filter(~Q(inventory__lt=99))
    # products = Product.objects.filter(id=F('inventory'))
    # products = Product.objects.all()[:40]
    # products = Product.objects.all()[20:50]
    # products = Product.objects.values('slug', 'description', 'unit_price').filter(name__icontains="oma").order_by('unit_price').reverse()
    # products = Product.objects.values('name', 'inventory').order_by('-inventory')
                        # p = Product.objects.earliest('unit_price')
                        # p = Product.objects.earliest('-unit_price')
                        # p = Product.objects.latest('unit_price')
                        # p = Product.objects.latest('-unit_price')
                        # p = Product.objects.latest('inventory', 'unit_price')
                        # latest هم مثل get فقط یه محصول به ما میده و بعد از latest دیگه نمیشه از
                        # filter و exclude و یا کوئری ست های مشابه استفاده کرد.
                        # print(p)
                        # context = {
                        #     'product': p
                        # }
    # products_at_least_ordered_for_once = OrderItem.objects.values('product').distinct()
    # products = Product.objects.filter(id__in=products_at_least_ordered_for_once)
    # print(list(products_at_least_ordered_for_once))
    # products = Product.objects.filter(order_items__gt=0) # این یکی رو خودم نوشتم با استفاده از ریلیتد نیم که خیلی باحاله :D
    # products = Product.objects.values_list('name', 'inventory').order_by('-inventory')
    # print(list(products))
    # products = Product.objects.only('id', 'name', 'description', 'unit_price')
    # products = Product.objects.defer('datetime_created', 'datetime_modified', 'category', 'discounts')
    # products = Product.objects.select_related('category').only('id', 'name', 'description', 'unit_price', 'category')
    # q = OrderItem.objects.select_related('order','product').all() # تمرینی که داده بود رو خودم بیشترش رو گرفتم. دیدم این طوری درست کار میکنه. میشه ۲ بار هم سلکت ریلیتد رو صدا کرد.
    # q = OrderItem.objects.select_related('order').select_related('product').all()
    # products = Product.objects.select_related('category').only('id', 'name', 'description', 'unit_price', 'category')
    # products = Product.objects.select_related('category').only('id', 'name', 'description', 'unit_price', 'category', 'category__title', 'category__description')
    # products = Product.objects.prefetch_related('order_items').all()
    # comments = Comment.objects.only('name', 'status', 'product').select_related('product') # Tamrin 1
    # print(len(comments))
    # context = {
    #     'comments': comments
    # }
    # products = Product.objects.all().select_related('category').prefetch_related('comments') # Tamrin 2
    # print(len(products))
    # context = {
    #     'products': products
    # }
    # orders = Order.objects.all().prefetch_related('items__product').select_related('customer') # Tamrin 3
    # print(len(orders))
    # context = {
    #     'orders': orders
    # }
    # products = Product.objects.aggregate(Avg('unit_price'))
    # products = Product.objects.aggregate(count=Count('id'), avg=Avg('unit_price'), max_inventory=Max('inventory'))
    # q = Product.objects.filter(inventory__gt=10).aggregate(count=Count('id'), avg=Avg('unit_price')) # Tamrin 1
    # q = OrderItem.objects.filter(product=1015).aggregate(Count('id')) # Tamrin 2 ravesh avval
    # Tamrin 2 raveshe dovvom. mitoonim az manager e related name i ke dade boodim estefade konim. mesle 2 khatte zir
    # product = Product.objects.get(id=1015)
    # q = product.order_items.aggregate(Count('id'))
    # Tamrin 3 do khatte ba'd
    q = OrderItem.objects.values('product_id').distinct().count()
    q = Product.objects.count()-q
    # Tamrin 4 خونه حل کنم.
    # چه تعداد پروداکت هستند که در سال ۲۰۲۲ فروش رفتند.           
    print(q)
    context = {
        'products': 'alaki error nade'
    }
    # customers = Customer.objects.filter(birth_date__isnull=True)
    # context['customers']=customers
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