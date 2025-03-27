from rest_framework import serializers
from rest_framework.serializers import Serializer, CharField
from .models import Retailer

class RetailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retailer
        fields = ['id', 'username', 'password', 'store_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        retailer = Retailer(**validated_data)
        retailer.set_password(password)
        retailer.save()
        return retailer


class ChangePasswordSerializer(Serializer):
    old_password = CharField(required=True)
    new_password = CharField(required=True)
