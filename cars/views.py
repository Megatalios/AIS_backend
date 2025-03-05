from django.shortcuts import render
from django.http import JsonResponse
from .models import Car  # Импорт модели Car из cars.models
from users.models import User # Импорт User, так как Car связан с User
from django.views.decorators.csrf import csrf_exempt
import json


# Получить машину по VIN номеру:
def get_car(request, vin_number):
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
    

def get_cars_by_brand(request, brand_query):
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


#@csrf_exempt - защита csrf-куки (не сливки шоу)
def add_car(request):
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


#@csrf_exempt
def update_car(request, car_id): # car_id передается в URL
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


#@csrf_exempt 
def delete_car(request, car_id): # car_id в URL
    if request.method == 'DELETE': # Используем DELETE метод
        try:
            car = Car.objects.get(id=car_id)
            car.delete() # Удаляем автомобиль
            return JsonResponse({'message': 'Car deleted successfully', 'car_id': car_id})
        except Car.DoesNotExist:
            return JsonResponse({'error': 'Car not found'}, status=404)
    else:
        return JsonResponse({'error': 'Only DELETE method allowed'}, status=405)