from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', views.CustomerRegistrationView.as_view(), name='customer_register'),
    path('login/', views.CustomerLoginView.as_view(), name='customer_login'),
    path('profile/', views.CustomerProfileView.as_view(), name='customer_profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]