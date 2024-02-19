from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True)
    top_product = models.ForeignKey(to='Product', on_delete=models.SET_NULL, null=True, related_name='+')

class Discount(models.Model):
    discount = models.FloatField()
    description = models.CharField(max_length=255)

class Product(models.Model):
    name = models.CharField(max_length=255) 
    category = models.ForeignKey(to=Category, on_delete=models.PROTECT, related_name='products')
    slug = models.SlugField()
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    discounts = models.ManyToManyField(to=Discount, blank=True)

class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=30)
    birth_date = models.DateField(null=True, blank=True)

class Address(models.Model):
    customer = models.OneToOneField(to=Customer, on_delete=models.CASCADE, primary_key=True)
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)

class OrderManager(models.Manager):
    def get_by_status(self, status='u'):
        if status==Order.ORDER_STATUS_UNPAID:
            return self.get_queryset().filter(status=Order.ORDER_STATUS_UNPAID)
        if status==Order.ORDER_STATUS_PAID:
            return self.get_queryset().filter(status=Order.ORDER_STATUS_PAID)
        if status==Order.ORDER_STATUS_CANCELED:
            return self.get_queryset().filter(status=Order.ORDER_STATUS_CANCELED)
        raise TypeError("You should only choose one of theese stats:\nu (for unpaid), p (for paid) or c (for canceled)!")


class UnpaidOrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Order.ORDER_STATUS_UNPAID)

class Order(models.Model):
    ORDER_STATUS_PAID = 'p'
    ORDER_STATUS_UNPAID = 'u'
    ORDER_STATUS_CANCELED = 'c'
    ORDER_STATUS = [
        (ORDER_STATUS_PAID, 'Paid'),
        (ORDER_STATUS_UNPAID, 'Unpaid'),
        (ORDER_STATUS_CANCELED, 'Canceled'),
    ]

    customer = models.ForeignKey(to=Customer, on_delete=models.PROTECT, related_name='orders')
    datetime_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=ORDER_STATUS, default=ORDER_STATUS_UNPAID)

    objects=OrderManager()
    mymanager=OrderManager()
    unpaid_manager=UnpaidOrderManager()

class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = [['order', 'product']]

class CommentManager(models.Manager):
    def get_approved(self):
        return self.get_queryset().filter(status=Comment.COMMENT_STATUS_APPROVED)

    def get_not_approved(self):
        return self.get_queryset().filter(status=Comment.COMMENT_STATUS_NOT_APPROVED)

    def get_waiting(self):
        return self.get_queryset().filter(status=Comment.COMMENT_STATUS_WAITING)

class ApprovedCommentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Comment.COMMENT_STATUS_APPROVED)

class Comment(models.Model):
    COMMENT_STATUS_WAITING = 'w'
    COMMENT_STATUS_APPROVED = 'a'
    COMMENT_STATUS_NOT_APPROVED = 'na'
    COMMENT_STATUS = [
        (COMMENT_STATUS_WAITING, 'Waiting'),
        (COMMENT_STATUS_APPROVED, 'Approved'),
        (COMMENT_STATUS_NOT_APPROVED, 'Not Approved'),
    ]

    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=255)
    body = models.TextField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=COMMENT_STATUS, default=COMMENT_STATUS_WAITING)

    objects = CommentManager()
    myobjects = CommentManager()
    approved_manager = ApprovedCommentManager()

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = [['cart', 'product']]

