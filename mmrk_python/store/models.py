from django.db import models
from django.contrib.auth.models import User


# Customer model
class Customer(models.Model):
    """Each customer model holds one to one relatioship to each user."""
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# Product model
class Product(models.Model):
    """Represents store product. Parent of OrderItem."""
    name = models.CharField(max_length=80)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url


# Order model
class Order(models.Model):
    """Represents the transaction that is placed or pending. 
    Holds transaction's ID, order status. Parent of OrderItem."""
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True) 
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=50, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


# Order's item model
class OrderItem(models.Model):
    """Represents order's single item. Child of the product and order models."""
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


# Shipping model
class ShippingAddress(models.Model):
    """Represents order's shipping information."""
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=50, null=False)
    city = models.CharField(max_length=50, null=False)
    state = models.CharField(max_length=50, null=False)
    zipcode = models.CharField(max_length=10, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address