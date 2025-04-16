from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Authentication endpoints
    path('login/', views.LoginView.as_view(), name='login'),
    path('customers/register/', views.CustomerRegistrationView.as_view(), name='customer_register'),
    path('retailers/register/', views.RetailerRegistrationView.as_view(), name='retailer_register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
