from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render
from .models import Product
from .serializers import ProductSerializer

# 1️⃣ Create Product API


class CreateProductView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(retailer=self.request.user)

# 2️⃣ List All Products API


class ListProductsView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# 3️⃣ Retrieve Single Product API


class RetrieveProductView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# 4️⃣ Update Product API (Only Owner Can Update)


class UpdateProductView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Product.objects.filter(retailer=self.request.user)

# 5️⃣ Delete Product API (Only Owner Can Delete)


class DeleteProductView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Product.objects.filter(retailer=self.request.user)

# 6️⃣ Custom Bouquets API


class CustomBouquetsView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        # Filter products that are custom bouquets
        # Assuming there's a 'is_custom_bouquet' field or similar category field
        return Product.objects.filter(is_custom_bouquet=True)

# 7️⃣ Custom Bouquets Template View


def custom_bouquets_view(request):
    """View for rendering the custom bouquets HTML template"""
    # Get available custom options from the database
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

    return render(request, 'custom_bouquets.html', context)
