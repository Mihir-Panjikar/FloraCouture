from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from customers.models import Customer
from retailers.models import Retailer

# Customer serializers
class CustomerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = Customer
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'phone_number', 'address']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False}
        }
    
    def create(self, validated_data):
        customer = Customer.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        # Add optional fields if provided
        if 'phone_number' in validated_data:
            customer.phone_number = validated_data['phone_number']
        if 'address' in validated_data:
            customer.address = validated_data['address']
        
        # Set password and save
        customer.set_password(validated_data['password'])
        customer.save()
        return customer

# Retailer serializers
class RetailerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = Retailer
        fields = ['id', 'username', 'email', 'password', 'store_name', 'business_name', 'phone_number', 'address']
    
    def create(self, validated_data):
        retailer = Retailer.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            store_name=validated_data['store_name'],
            business_name=validated_data['business_name'],
            phone_number=validated_data['phone_number'],
            address=validated_data['address'],
            is_verified=False  # Retailers start unverified by default
        )
        
        # Set password and save
        retailer.set_password(validated_data['password'])
        retailer.save()
        return retailer
