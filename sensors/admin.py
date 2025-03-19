from django.contrib import admin

from .models import SensorData  # Импортируй нужные модели

admin.site.register(SensorData)  # Регистрируем модель в админке


