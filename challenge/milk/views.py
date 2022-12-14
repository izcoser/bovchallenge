from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from milk.models import Farm, Farmer, MilkDeliveries, Cost
from milk.serializers import FarmSerializer, FarmerSerializer, DeliverySerializer, CostSerializer
from django.db.models import Sum

@csrf_exempt
def costs(request):
    """
    List all costs associated with first and second semesters with GET
    Or create new cost with POST.
    """
    if request.method == 'GET':
        costs = Cost.objects.all()
        serializer = CostSerializer(costs, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

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

# Obt??m os custos (base, por km, b??nus) relacionados a um m??s.
def get_costs(month):
    if month <= 6:
        return Cost.objects.filter(semester=1).first()
    else:
        return Cost.objects.filter(semester=2).first()

# Obt??m o volume de leite entregue dado um c??digo de fazenda e um m??s.
def get_volume(farm_code, month, year):
    deliveries = MilkDeliveries.objects.filter(farm__code=farm_code, date__month=month, date__year=year)
    return deliveries.aggregate(Sum('amount'))['amount__sum'] or 0

# Verifica se o c??digo do fazendeiro e m??s s??o v??lidos.
def check_inputs(farmer_code, month, year):
    if farmer_code == None or month == None or month > 12 or month < 1 or year == None:
        return JsonResponse({'error': 'Must specify farmer code, month (1 to 12) and year.'})

# Calcula o pre??o do litro de leite para uma fazenda em um m??s.
def milk_price(farm_code, month, year):
    costs = get_costs(month)
    volume = get_volume(farm_code, month, year)

    try:
        farm = Farm.objects.get(code=farm_code)
    except Farm.DoesNotExist:
        raise Exception(f'Farm {farm_code} does not exist.')
    
    distance = farm.distance
    distance_under_50 = min(50, distance)
    distance_over_50 = max(distance - 50, 0)
    volume_over_10k = max(volume - 10000, 0)
    price = volume * costs.base - (distance_under_50 * costs.under_50 + distance_over_50 * costs.over_50)\
    + costs.bonus * volume_over_10k
    
    return price, volume

# Calcula o pre??o do litro de leite para um fazendeiro em um m??s.
def farmer_milk_price(farmer_code, month, year):
    # Um fazendeiro pode ter v??rias fazendas, nesse caso vamos fazer uma m??dia aritm??tica
    # para obter o pre??o.
    farms = Farm.objects.filter(owner__code=farmer_code)
    numerator = 0
    denominator = 0
    for f in farms:
        price, volume = milk_price(f.code, month, year)
        numerator += price * volume
        denominator += volume
    if denominator == 0:
        return -1 # n??o produziu
    else:
        return numerator / denominator

# Recebe um pre??o e retorna um dict com pre??o em formato brasileiro e ingl??s.
def format_price(price):
    price_en = f'{price:,.2f}'
    price_br = price_en.replace('.', '_').replace(',', '.').replace('_', ',')
    return {
            'price_en': price_en,
            'price_br': price_br
            }

@csrf_exempt
def farmer_output(request, farmer_code=None, month=None, year=None):
    check_inputs(farmer_code, month, year)

    deliveries = MilkDeliveries.objects.filter(farm__owner__code=farmer_code, date__month=month, date__year=year)
    volumes = {str(i.date): i.amount for i in deliveries}
    monthly_total = deliveries.aggregate(Sum('amount'))['amount__sum'] or 0
    monthly_average = monthly_total / 30
    volumes['monthly_average'] = round(monthly_average, 2)

    return JsonResponse(volumes)

@csrf_exempt
def farmer_monthly_price(request, farmer_code=None, month=None, year=None):
    check_inputs(farmer_code, month, year)
    price = farmer_milk_price(farmer_code, month, year)

    if price == -1:
        return JsonResponse({'No volume': 'No volume.'})
    else:
        return JsonResponse(format_price(price))

@csrf_exempt
def farmer_yearly_price(request, farmer_code=None, year=None):
    if farmer_code == None or year == None:
        return JsonResponse({'error': 'Must specify farmer code and year.'})
    print('heloooooooooooooooo')
    prices = {}
    for i in range(1, 13):
        p = farmer_milk_price(farmer_code, i, year)
        prices[i] = format_price(p) if p != -1 else 'No volume.'
    
    return JsonResponse(prices)