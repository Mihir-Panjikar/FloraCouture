from django.urls import path
from . import views

urlpatterns = [
    # Main page routes
    path('', views.index, name='index'),
    path('custom-bouquets/', views.custom_bouquets, name='custom_bouquets'),
    path('simple-bouquets/', views.simple_bouquets, name='simple_bouquets'),
    path('cart/', views.cart, name='cart'),
    path('contact/', views.contact, name='contact'),
    path('thank-you/', views.thank_you, name='thank_you'),

    # Fallback route for static files (development only)
    path('static/<path:path>', views.serve_static, name='serve_static'),
]
