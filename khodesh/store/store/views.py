from django.shortcuts import render

from .models import Product, Customer

def show_data(request):
    products = Product.objects.filter(category__title__contains="sa")
    # q = Customer.objects.filter(birth_date__isnull=True)
    # context = {
    #     'customers': q
    # }
    print(len(products))
    context = {
        'products': products
    }
    return render(request, 'welcome.html', context)