from django.urls import path
from .views import RetailerRegisterView, RetailerProfileView, RetailerProfileUpdateView, LogoutRetailer

urlpatterns = [
    path('register/', RetailerRegisterView.as_view(), name='retailer-register'),
    path('profile/', RetailerProfileView.as_view(), name='retailer-profile'),
    path('profile/update/', RetailerProfileUpdateView.as_view(), name='retailer-profile-update'),
    path('logout/', LogoutRetailer.as_view(), name='retailer-logout'),

]
