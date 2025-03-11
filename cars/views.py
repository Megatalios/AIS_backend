from django.shortcuts import render
from django.http import JsonResponse
from .models import Car  # Импорт модели Car из cars.models
from users.models import User # Импорт User, так как Car связан с User
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework import serializers




@api_view(['GET'])
def get_all_cars(request):
    """Получить все машины"""
    all_cars = Car.objects.all()
    cars_list = []
    for car in all_cars:
        cars_list.append({
            'id': car.id, 
            'vin_number': car.vin_number, 
            'brand': car.brand,
            'color': car.color,
            'owner_id': car.owner.id if car.owner else None # Если owner не None, то вернуть id, если None, то вернуть None
            })
    return JsonResponse({'cars': cars_list})


@api_view(['GET'])
def get_car(request, vin_number):
    """Получить машину по VIN номеру"""
    try:
        car = Car.objects.get(vin_number=vin_number)
        car_data = {
            'id': car.id,
            'vin_number': car.vin_number,
            'brand': car.brand,
            'color': car.color,
            'owner_id': car.owner.id if car.owner else None
        }
        return JsonResponse(car_data)
    except Car.DoesNotExist:
        return JsonResponse({'error': 'Car not found, works'}, status=404)
    
@api_view(['GET'])
def get_cars_by_brand(request, brand_query):
    """Получить все машины по заданному бренду"""
    cars = Car.objects.filter(brand__iexact=brand_query) # __iexact - совпадение без учета регистра
    cars_data = []
    for car in cars:
        cars_data.append({
            'id': car.id,
            'vin_number': car.vin_number,
            'brand': car.brand,
            'color': car.color,
            'owner_id': car.owner.id if car.owner else None
        })
    return JsonResponse({'cars': cars_data})

# Сериализатор для описания тела запроса
class CarSerializer(serializers.Serializer):
    # vin_number = serializers.CharField()
    # color = serializers.CharField()
    # brand = serializers.CharField()

    vin_number = serializers.RegexField(
        regex=r'^[A-HJ-NPR-Z0-9]{17}$',
        error_messages={"invalid": "VIN-номер должен состоять из 17 символов (латинские буквы и цифры), без I, O, Q."}
    )
    color = serializers.RegexField(
        regex=r'^[A-Za-z\s-]+$',
        error_messages={"invalid": "Название цвета должно содержать только буквы."}
    )
    brand = serializers.CharField(min_length=2, max_length=50)

    owner_id = serializers.IntegerField()

    class Meta:
        model = Car
        fields = ['id', 'vin_number', 'brand', 'color', 'owner_id']

@swagger_auto_schema(
    method='POST',
    request_body=CarSerializer,  # Указываем сериализатор для тела запроса
    responses={200: 'Car added successfully'}
)
@api_view(['POST'])
#@csrf_exempt - защита csrf-куки (не сливки шоу)
def add_car(request):
    """Добавить новую машину"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            vin_number = data.get('vin_number')
            brand = data.get('brand')
            color = data.get('color')
            owner_id = data.get('owner_id') # ID владельца

            if not vin_number or not brand or not color:
                return JsonResponse({'error': 'VIN, brand and color are required'}, status=400)

            try:
                owner = User.objects.get(id=owner_id) if owner_id else None # Получаем владельца по ID или None
            except User.DoesNotExist:
                return JsonResponse({'error': 'Owner not found'}, status=400)

            car = Car(vin_number=vin_number, brand=brand, color=color, owner=owner)
            car.save()
            return JsonResponse({'message': 'Car created successfully', 'car_id': car.id}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)

@swagger_auto_schema(
    method='PUT',
    request_body=CarSerializer,  # Указываем сериализатор для тела запроса
    responses={200: 'Car updated successfully'}
)
@api_view(['PUT'])
#@csrf_exempt
def update_car(request, car_id): # car_id передается в URL
    """Обновить существующую машину"""
    if request.method == 'PUT': # Используем PUT для обновления
        try:
            data = json.loads(request.body)
            vin_number = data.get('vin_number')
            brand = data.get('brand')
            color = data.get('color')
            owner_id = data.get('owner_id')

            try:
                car = Car.objects.get(id=car_id) # Находим автомобиль по ID
            except Car.DoesNotExist:
                return JsonResponse({'error': 'Car not found'}, status=404)

            if vin_number:
                car.vin_number = vin_number
            if brand:
                car.brand = brand
            if color:
                car.color = color
            if owner_id: # Обновляем владельца, если передан owner_id
                try:
                    owner = User.objects.get(id=owner_id)
                    car.owner = owner
                except User.DoesNotExist:
                    return JsonResponse({'error': 'Owner not found'}, status=400) # Ошибка, если указан несуществующий владелец

            car.save() # Сохраняем изменения
            return JsonResponse({'message': 'Car updated successfully', 'car_id': car.id})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        else:
            return JsonResponse({'error': 'Only PUT method allowed'}, status=405)

@api_view(['DELETE'])
#@csrf_exempt 
def delete_car(request, car_id): # car_id в URL
    """Удалить машину по ID"""
    if request.method == 'DELETE': # Используем DELETE метод
        try:
            car = Car.objects.get(id=car_id)
            car.delete() # Удаляем автомобиль
            return JsonResponse({'message': 'Car deleted successfully', 'car_id': car_id})
        except Car.DoesNotExist:
            return JsonResponse({'error': 'Car not found'}, status=404)
    else:
        return JsonResponse({'error': 'Only DELETE method allowed'}, status=405)