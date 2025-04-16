from django.shortcuts import render
from django.http import HttpResponse, FileResponse
import os
from django.conf import settings


def index(request):
    return render(request, 'index.html')


def cart(request):
    return render(request, 'cart.html')


def contact(request):
    return render(request, 'contact.html')


def custom_bouquets(request):
    # Custom bouquet options that can be loaded from the database
    custom_options = [
        {"name": "Chocolates", "price": 100},
        {"name": "Hotwheels", "price": 150},
        {"name": "Personalised Bouquet", "price": 200},
        {"name": "Heart-Shaped Bouquet", "price": 250},
        {"name": "Money Bouquet", "price": 300},
        {"name": "Ferrero Rocher", "price": 180},
    ]

    context = {
        'custom_options': custom_options,
        'base_price': 500
    }
    return render(request, 'custom-bouquets.html', context)


def simple_bouquets(request):
    return render(request, 'simple-bouquets.html')


def thank_you(request):
    return render(request, 'thank-you.html')


def serve_static(request, path):
    """
    Fallback function to serve static files if Django's static serving fails.
    Should only be used in development.
    """
    file_path = os.path.join(settings.STATICFILES_DIRS[0], path)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'))
    return HttpResponse(status=404)
