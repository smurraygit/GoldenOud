from django.shortcuts import render
from store.models import Product


def home(requst):
    products = Product.objects.all().filter(is_available=True)

    context = {
        'products': products,
    }
    return render(requst, 'home.html', context)
