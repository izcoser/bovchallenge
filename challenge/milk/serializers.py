from rest_framework import serializers
from milk.models import Farmer, Farm, MilkDeliveries, Cost

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

class CostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cost
        fields = ['id', 'base', 'under_50', 'over_50', 'bonus', 'semester']