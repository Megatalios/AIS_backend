from django.db import models
from django.core.validators import RegexValidator
from users.models import User  # Импорт модели User из приложения users

# Валидатор VIN-номера
vin_validator = RegexValidator(
    regex=r'^[A-HJ-NPR-Z0-9]{17}$',
    message="VIN-номер должен состоять из 17 символов (латинские буквы и цифры), без I, O, Q."
)

class Car(models.Model):
    vin_number = models.CharField(
        max_length=17,  # VIN всегда 17 символов
        unique=True,
        validators=[vin_validator]  # Применяем валидатор
    )  
    color = models.CharField(
        max_length=30,  # Реалистичный лимит
        validators=[RegexValidator(regex=r'^[A-Za-z\s-]+$', message="Название цвета должно содержать только буквы")]
    )  
    brand = models.CharField(
        max_length=50
    ) 

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')  # Внешний ключ к User

    def __str__(self):
        return f"{self.brand} ({self.vin_number})"  # Отображение марки и VIN в админке и т.д.
