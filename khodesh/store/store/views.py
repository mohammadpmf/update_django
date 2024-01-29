from django.shortcuts import render


def welcome(request):
    a=2
    b=3
    print('test')
    return render(request, 'welcome.html')