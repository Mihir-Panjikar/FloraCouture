from django.urls import path
from .views import (
    CreateProductView,
    ListProductsView,
    RetrieveProductView,
    UpdateProductView,
    DeleteProductView
)

urlpatterns = [
    path("create/", CreateProductView.as_view(), name="create_product"),
    path("list/", ListProductsView.as_view(), name="list_products"),
    path("<int:pk>/", RetrieveProductView.as_view(), name="retrieve_product"),
    path("<int:pk>/update/", UpdateProductView.as_view(), name="update_product"),
    path("<int:pk>/delete/", DeleteProductView.as_view(), name="delete_product"),
]
