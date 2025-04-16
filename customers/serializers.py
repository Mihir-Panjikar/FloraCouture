from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Customer

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
        # Create customer instance
        customer = Customer.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', ''),
            address=validated_data.get('address', '')
        )
        
        # Set password and save
        customer.set_password(validated_data['password'])
        customer.save()
        return customer
        
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'address']
        read_only_fields = ['username', 'email']  # These shouldn't be changed via this serializer