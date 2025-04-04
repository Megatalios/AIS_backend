from django.shortcuts import render
from django.http import JsonResponse
from .models import SensorData # Импорт модели SensorData из sensors.models
from cars.models import Car     # Импорт Car, так как SensorData связан с Car
from users.models import User    # Импорт User, так как SensorData связан с User
from django.views.decorators.csrf import csrf_exempt
import json
import datetime

# Ищем данные по датчикам по ID
def get_sensor_data(request, sensor_data_id):
    try:
        sensor_data = SensorData.objects.get(id=sensor_data_id)
        sensor_data_dict = { # Преобразуем объект SensorData в словарь для JSON
            'id': sensor_data.id,
            'timestamp': sensor_data.timestamp.isoformat(), # Сериализуем datetime в строку ISO format
            'engine_rpm': sensor_data.engine_rpm,
            'intake_air_temperature': sensor_data.intake_air_temperature,
            'mass_air_flow_sensor': sensor_data.mass_air_flow_sensor,
            'injection_duration': sensor_data.injection_duration,
            'throttle_position': sensor_data.throttle_position,
            'vehicle_speed': sensor_data.vehicle_speed,
            'manifold_absolute_pressure': sensor_data.manifold_absolute_pressure,
            'user_id': sensor_data.user.id if sensor_data.user else None,
            'car_id': sensor_data.car.id if sensor_data.car else None,
        }
        return JsonResponse(sensor_data_dict)
    except SensorData.DoesNotExist:
        return JsonResponse({'error': 'SensorData not found'}, status=404)

# Ищем данные по датчикам по VIN-номеру автомобиля
def get_sensor_data_for_car(request, car_vin):
    try:
        car = Car.objects.get(vin_number=car_vin)
        sensor_data_list = car.sensor_data.all() # Получаем все SensorData, связанные с car через relation
        sensor_data_records = []
        for data in sensor_data_list:
            sensor_data_records.append({
                'id': data.id,
                'timestamp': data.timestamp.isoformat(),
                'engine_rpm': data.engine_rpm,
                # ... (остальные поля SensorData) ...
            })
        return JsonResponse({'sensor_data': sensor_data_records})
    except Car.DoesNotExist:
        return JsonResponse({'error': 'Car not found'}, status=404)
    
#
@csrf_exempt
def add_sensor_data_record(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            car_vin = data.get('car_vin')
            user_id = data.get('user_id')
            engine_rpm = data.get('engine_rpm')
            intake_air_temperature = data.get('intake_air_temperature')
            mass_air_flow_sensor = data.get('mass_air_flow_sensor')
            injection_duration = data.get('injection_duration')
            throttle_position = data.get('throttle_position')
            vehicle_speed = data.get('vehicle_speed')
            manifold_absolute_pressure = data.get('manifold_absolute_pressure')

            if not car_vin or not user_id or engine_rpm is None: # engine_rpm - обязательное поле
                return JsonResponse({'error': 'Car VIN, User ID and engine_rpm are required'}, status=400)

            try:
                car = Car.objects.get(vin_number=car_vin)
            except Car.DoesNotExist:
                return JsonResponse({'error': 'Car not found'}, status=400)
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=400)

            sensor_data = SensorData(
                car=car, 
                user=user,
                timestamp=datetime.datetime.now(), # Timestamp можно задать явно или Django установит автоматически
                engine_rpm=engine_rpm,
                intake_air_temperature=intake_air_temperature,
                mass_air_flow_sensor=mass_air_flow_sensor,
                injection_duration=injection_duration,
                throttle_position=throttle_position,
                vehicle_speed=vehicle_speed,
                manifold_absolute_pressure=manifold_absolute_pressure
            )
            sensor_data.save()
            return JsonResponse({'message': 'SensorData record created successfully', 'sensor_data_id': sensor_data.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)
    
#
@csrf_exempt
def update_sensor_data_record(request, sensor_data_id): # sensor_data_id передается в URL
    if request.method == 'PUT': # Используем PUT для обновления
        try:
            data = json.loads(request.body)
            engine_rpm = data.get('engine_rpm')
            intake_air_temperature = data.get('intake_air_temperature')
            mass_air_flow_sensor = data.get('mass_air_flow_sensor')
            injection_duration = data.get('injection_duration')
            throttle_position = data.get('throttle_position')
            vehicle_speed = data.get('vehicle_speed')
            manifold_absolute_pressure = data.get('manifold_absolute_pressure')
            car_vin = data.get('car_vin') # Можно обновить и автомобиль, к которому относятся данные
            user_id = data.get('user_id') # и пользователя

            try:
                sensor_data = SensorData.objects.get(id=sensor_data_id) # Находим запись данных датчика по ID
            except SensorData.DoesNotExist:
                return JsonResponse({'error': 'SensorData record not found'}, status=404)

            if engine_rpm is not None:
                sensor_data.engine_rpm = engine_rpm
            if intake_air_temperature is not None:
                sensor_data.intake_air_temperature = intake_air_temperature
            if mass_air_flow_sensor is not None:
                sensor_data.mass_air_flow_sensor = mass_air_flow_sensor
            if injection_duration is not None:
                sensor_data.injection_duration = injection_duration
            if throttle_position is not None:
                sensor_data.throttle_position = throttle_position
            if vehicle_speed is not None:
                sensor_data.vehicle_speed = vehicle_speed
            if manifold_absolute_pressure is not None:
                sensor_data.manifold_absolute_pressure = manifold_absolute_pressure
            if car_vin: # Обновляем автомобиль, если передан car_vin
                try:
                    car = Car.objects.get(vin_number=car_vin)
                    sensor_data.car = car
                except Car.DoesNotExist:
                    return JsonResponse({'error': 'Car not found'}, status=400) # Ошибка, если указан несуществующий автомобиль
            if user_id: # Обновляем пользователя, если передан user_id
                try:
                    user = User.objects.get(id=user_id)
                    sensor_data.user = user
                except User.DoesNotExist:
                    return JsonResponse({'error': 'User not found'}, status=400) # Ошибка, если указан несуществующий пользователь

            sensor_data.save() # Сохраняем изменения
            return JsonResponse({'message': 'SensorData record updated successfully', 'sensor_data_id': sensor_data.id})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        else:
            return JsonResponse({'error': 'Only PUT method allowed'}, status=405)

#
@csrf_exempt
def delete_sensor_data_record(request, sensor_data_id): # sensor_data_id в URL
    if request.method == 'DELETE': # Используем DELETE метод
        try:
            sensor_data = SensorData.objects.get(id=sensor_data_id)
            sensor_data.delete() # Удаляем запись данных датчика
            return JsonResponse({'message': 'SensorData record deleted successfully', 'sensor_data_id': sensor_data_id})
        except SensorData.DoesNotExist:
            return JsonResponse({'error': 'SensorData record not found'}, status=404)
    else:
        return JsonResponse({'error': 'Only DELETE method allowed'}, status=405)
