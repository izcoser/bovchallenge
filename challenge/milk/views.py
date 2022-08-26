from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from milk.models import Farm, Farmer, MilkDeliveries, Cost
from milk.serializers import FarmSerializer, FarmerSerializer, DeliverySerializer
from django.db.models import Sum

@csrf_exempt
def farmer_list(request):
    """
    List all farmers with GET or create new farmer with POST.
    """
    if request.method == 'GET':
        farmers = Farmer.objects.all()
        serializer = FarmerSerializer(farmers, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = FarmerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def farm_list(request):
    """
    List all farms with GET or create new farm with POST.
    """
    if request.method == 'GET':
        farms = Farm.objects.all()
        serializer = FarmSerializer(farms, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = FarmSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def deliveries_list(request):
    """
    List all deliveries with GET or create new delivery with POST.
    """
    if request.method == 'GET':
        deliveries = MilkDeliveries.objects.all()
        serializer = DeliverySerializer(deliveries, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DeliverySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def get_costs(month):
    if month <= 6:
        cost = Cost.objects.filter(semester=1)
    else:
        cost = Cost.objects.filter(semester=1)

@csrf_exempt
def farmer_output(request, farmer_code=None, month=None):
    if farmer_code == None or month == None or month > 12 or month < 1:
        return JsonResponse({'error': 'Must specify farmer primary key and month (1 to 12).'})
    
    deliveries = MilkDeliveries.objects.filter(farm__owner__code=farmer_code, date__month=month)
    volumes = {str(i.date): i.amount for i in deliveries}
    monthly_total = deliveries.aggregate(Sum('amount'))['amount__sum'] or 0
    monthly_average = monthly_total / 30
    volumes['monthly_average'] = round(monthly_average, 2)

    return JsonResponse(volumes)

@csrf_exempt
def farmer_output(request, farmer_code=None, month=None):
    if farmer_code == None or month == None or month > 12 or month < 1:
        return JsonResponse({'error': 'Must specify farmer primary key and month (1 to 12).'})
    
    deliveries = MilkDeliveries.objects.filter(farm__owner__code=farmer_code, date__month=month)
    volumes = {str(i.date): i.amount for i in deliveries}
    monthly_total = deliveries.aggregate(Sum('amount'))['amount__sum'] or 0
    monthly_average = monthly_total / 30
    volumes['monthly_average'] = round(monthly_average, 2)

    return JsonResponse(volumes)

@csrf_exempt
def farmer_monthly_price(request, farmer_code=None, month=None):
    if farmer_code == None or month == None or month > 12 or month < 1:
        return JsonResponse({'error': 'Must specify farmer primary key and month (1 to 12).'})
    
    deliveries = MilkDeliveries.objects.filter(farm__owner__code=farmer_code, date__month=month)
    volumes = {str(i.date): i.amount for i in deliveries}
    monthly_total = deliveries.aggregate(Sum('amount'))['amount__sum'] or 0
    monthly_average = monthly_total / 30
    volumes['monthly_average'] = round(monthly_average, 2)

    return JsonResponse(volumes)