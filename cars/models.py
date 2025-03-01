from django.db import models
from users.models import User # Импорт модели User из приложения users

class Car(models.Model):
    vin_number = models.CharField(max_length=20, unique=True) # VIN-номер, строка, уникальный
    color = models.CharField(max_length=50) # Цвет автомобиля, строка
    brand = models.CharField(max_length=100) # Марка автомобиля, строка
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars') # Внешний ключ к User, связь "многие-к-одному"

    def __str__(self):
        return f"{self.brand} ({self.vin_number})" # Отображение марки и VIN в админке и т.д.