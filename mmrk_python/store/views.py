from django.shortcuts import render
from .models import Customer, Product, Order, OrderItem, ShippingAddress


# Store page view
def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, "store/store.html", context)


# Cart page view
def cart(request):
    context = {}
    return render(request, "store/cart.html", context)


# Checkout page view
def checkout(request):
    context = {}
    return render(request, "store/checkout.html", context)