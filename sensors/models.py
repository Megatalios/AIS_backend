from django.db import models
from users.models import User # Импорт модели User
from cars.models import Car   # Импорт модели Car

class SensorData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True) # Временная метка, автоматически добавляется при создании записи
    engine_rpm = models.FloatField() # Обороты двигателя, число с плавающей точкой
    intake_air_temperature = models.FloatField() # Температура воздуха на впуске
    mass_air_flow_sensor = models.FloatField(null=True, blank=True) # MAF, может быть пустым (если датчика нет)
    injection_duration = models.FloatField(null=True, blank=True) # Длительность впрыска, может быть пустым
    throttle_position = models.FloatField(null=True, blank=True) # Положение дроссельной заслонки, может быть пустым
    vehicle_speed = models.FloatField(null=True, blank=True) # Скорость автомобиля, может быть пустым
    manifold_absolute_pressure = models.FloatField(null=True, blank=True) # Давление во впускном коллекторе, может быть пустым

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sensor_data') # Внешний ключ к User
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='sensor_data') # Внешний ключ к Car

    def __str__(self):
        return f"Sensor Data for Car: {self.car.brand} VIN: {self.car.vin_number} at {self.timestamp}" # Отображение в админке