from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100) # Имя пользователя, строка, макс. длина 100 символов
    email = models.EmailField(unique=True) # Электронная почта, должна быть уникальной

    def __str__(self):
        return self.name # Отображение имени пользователя в админке и т.д.