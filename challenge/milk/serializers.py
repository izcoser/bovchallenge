from rest_framework import serializers
from milk.models import Farmer, Farm, MilkDeliveries

class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = ['id', 'name', 'code', 'cnpj']

class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = ['id', 'name', 'code', 'distance', 'owner']

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = MilkDeliveries
        fields = ['id', 'farm', 'amount', 'date']
