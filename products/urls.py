from django.urls import path
from .views import (
    CreateProductView,
    ListProductsView,
    RetrieveProductView,
    UpdateProductView,
    DeleteProductView,
    custom_bouquets_view  # Adjust import based on your actual view function
)

urlpatterns = [
    path("create/", CreateProductView.as_view(), name="create_product"),
    path("list/", ListProductsView.as_view(), name="list_products"),
    path("<int:pk>/", RetrieveProductView.as_view(), name="retrieve_product"),
    path("<int:pk>/update/", UpdateProductView.as_view(), name="update_product"),
    path("<int:pk>/delete/", DeleteProductView.as_view(), name="delete_product"),
    path('custom-bouquets/', custom_bouquets_view, name='custom_bouquets'),
]
