from django.shortcuts import render
from django.db.models import Q, F
from django.db.models import Count, Avg, Sum, Min, Max
from django.db.models import Value, Func, ExpressionWrapper, DecimalField

from .models import Product, Customer, OrderItem, Order, Comment, Category

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
    # q = OrderItem.objects.values('product_id').distinct().count()
    # q = Product.objects.count()-q
    # Tamrin 4
    # q = OrderItem.objects.filter(order__datetime_created__year=2024).count()
    # print(q)
    ##################################################################################

    # Annotation
    # products = Product.objects.all().annotate(price=F('unit_price'))[:2]
    # products = OrderItem.objects.all().annotate(total_price=F('unit_price')*F('quantity'))
    # products = Customer.objects.annotate(full_name = Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT')).defer('first_name', 'last_name')
    # products = Order.objects.annotate(items_count=Count('items'))
    # products = Customer.objects.annotate(number_of_orders=Count('orders'))
    # products = OrderItem.objects.annotate(total_price=ExpressionWrapper(F('quantity') * F('unit_price'), output_field=DecimalField()))
    # print(products)

    # Custom Manager # اسم منیجر ها رو دقت کنم چون عمدا چیزهای مختلف گذاشته بودم. یه جا
    # مای آبجکتز یه جا مای منیجر. بعدا ثابت از یه چیز استفاده کنم اما اینجا چون موقع 
    # آموزش بود عمدا این کار رو کردم.
    # products = Comment.myobjects.get_approved()
    # products = Comment.objects.all()
    # products = Order.mymanager.get_by_status('c')
    # products = Order.unpaid_manager.all()
    # print(list(products), len(list(products)))
    # context = {
    #     'products': products,
    # }

    # # create kardan
    # product = Product.objects.get(id=1001)
    # # ravesh 1 استفاده از منیجر
    # Comment.objects.create(
    #     name='Mohammad',
    #     body="Harchizi",
    #     product=product
    # )
    # # ravesh 2 ساخت یک نمونه از کلاس و صدا کردن تابع سیو
    # c = Comment()
    # c.name = "Amin"
    # c.body = "in ro amin sakhte"
    # c.product = product
    # c.save()

    # update kardan
    # ravesh 1 ke dg test nakardam. chon dorost nist.
    # در واقع ما یه نمونه از کلاس میسازیم که چون آی دیش تکراری هست، وقتی میخواد ذخیره
    # کنه، تازه اون موقع میبینه که این آی دی وجود داشت. پس جدید نمیسازه و همون قبلی
    # رو ویرایش میکنه. اما چون ما مثلا فقط بهش تایتل دادیم، بقیه فیلدها رو با استرینگ
    # خالی پر میکنه که باعث میشه یا اطلاعات بقیه فیلدها از بین برن یا اگه نالبل نیستند،
    # ارور بگیریم که هیچ حالتش خوب نیست.
    # c = Category(id=1001) # ya c = Category(pk=1001)
    # c.title='car'
    # c.save()

    # ravesh 2 ke dorost tar az avvali hast.
    # product = Product.objects.get(pk=1001)
    # این طوری از دیتابیس کل اون نمونه رو میگیریم و از اول آبجکت جدید نمیسازیم
    # بلکه رو همون قبلیه کار رو ادامه میدیم. حالا اگه فقط یه فیلد رو عوض کنیم
    # و به بقیه دست نزنیم، همون مقدار قبلی خودش رو داره و مشکلی پیش نمیاد.
    # c.title = 'car'
    # c = Category.objects.get(id=196)
    # c.top_product = product
    # c.save()
    # اما تو این روش ۲ تا کوئری میزنه به دیتابیس. حالا اگه بخوایم یه کوئری بزنه،
    # میتونیم از روش ۳ استفاده کنیم که استفاده از منیجر هست.
    
    # ravesh 3 
    # Category.objects.filter(id__range=(185, 192)).update(title='hello')
    # فقط خیلی دقت کنم. توضیح داد که موقع استفاده از آپدیت باید دقت کنیم
    # وگرنه کل دیتابیس به هم میریزه. خودم هم عمدا بدون فیلتر استفاده کردم زدم
    # همه عنوان ها رو عوض کرد. یه کوئری کمتر میزنه اما دقت بکنیم. تو مدل قبلی با 
    # get کار کردیم که فقط یه نمونه رو به ما میداد و اون رو سیو میکردیم.
    # اما روی یه دونه متد آپدیت رو نمیشه صدا کرد. حالت عادی اگه فقط تابع
    # آپدیت رو با منیجر صدا کنیم، به صورت پیش فرض روی همه عمل میکنه. خودمون
    # هم اگه فیلتر درستی ننویسیم ممکنه که چندین تا آیتم رو عوض کنه. دیلیت هم داره
    # که اون هم حتما همین مشکل رو داره. تنها تفاوت اینه که دیلیت رو میشه رو یه
    # دونه آبجکتی که با گِت گرفتیم صدا زد. اما آپدیت رو نمیشه و اسم آپدیت اونجا سیو
    # هست. اما روی کوئری ست ها هم آپدیت داریم هم دیلیت.

    # delete kardan
    # Category.objects.create(title='alaki') # واسه این که قبلی ها رو پاک نکنیم یه الکی ساختیم اول
    # raveshe avval با استفاده از منیجر که دقت کنیم حتما فیلتر درست بزنیم بعد پاک کنیم.
    # Category.objects.filter(title='alaki').delete()

    # raveshe dovvom
    # c = Category.objects.get(pk=204)
    # c.delete()

    # raveshe sevvom
    # اینجا برعکس آپدیت کردن بود و این یکی یه کوئری کمتر نسبت به روش دوم می فرستاد.
    # علاوه بر این روش دوم وقتی که اون آی دی وجود نداره ارور میده.
    # اما این یکی ارور نمیده. چون همون لحظه میسازه. اگه وجود داشته باشه که همونی
    # که وجود داشت رو پیدا میکنه و پاک میکنه و ارور نمیده. اگه وجود نداشته باشه هم
    # که چون جدید ساخته مشکلی نداره و همین جدیده رو پاک میکنه.
    # c = Category(pk=205)
    # c.delete()

    # Tamrin create update delete
    

    context = {
        'products': 'alaki error nade',
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