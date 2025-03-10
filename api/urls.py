from django.urls import path
from .views import RetailerRegisterView, RetailerLoginView

urlpatterns = [
    path('register/', RetailerRegisterView.as_view(), name='retailer-register'),
    path('login/', RetailerLoginView.as_view(), name='retailer-login'),

]
