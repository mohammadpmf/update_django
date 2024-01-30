from django.shortcuts import render

from .models import Product

def show_data(request):
    products = Product.objects.all()
    context = {
        'products': products[1:51]
    }
    return render(request, 'welcome.html', context)