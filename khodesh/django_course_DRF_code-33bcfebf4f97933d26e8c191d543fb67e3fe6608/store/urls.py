from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list),
    path('products/<int:pk>/', views.product_detail),

    path('addresses/', views.addresses_list),
    path('customers/', views.customers_list),
    path('orders/', views.orders_list),
    path('order_items/', views.order_items_list),
]
