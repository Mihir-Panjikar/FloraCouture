from rest_framework import serializers
from django.contrib.auth import get_user_model

Retailer = get_user_model()  # Get the custom Retailer model

class RetailerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = Retailer
        fields = ['username', 'email', 'password', 'business_name', 'phone_number', 'address']

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = Retailer.objects.create_user(password=password, **validated_data)
        return user
