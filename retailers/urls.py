from django.urls import path
from .views import (
    RetailerRegisterView, RetailerProfileView, RetailerProfileUpdateView, LogoutRetailer
    , LoginRetailer, RetailerListView, DeleteRetailerView, ChangePasswordView, ForgotPasswordView
)

urlpatterns = [
    path('register/', RetailerRegisterView.as_view(), name='retailer-register'),
    path("login/", LoginRetailer.as_view(), name="login"),
    path('profile/', RetailerProfileView.as_view(), name='retailer-profile'),
    path('profile/update/', RetailerProfileUpdateView.as_view(), name='retailer-profile-update'),
    path('logout/', LogoutRetailer.as_view(), name='retailer-logout'),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("retailers/", RetailerListView.as_view(), name="retailers_list"),
    path("delete-account/", DeleteRetailerView.as_view(), name="delete_account"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot_password"),

]
