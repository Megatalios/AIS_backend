from django.contrib import admin
from .models import Car  # Импортируй нужные модели

admin.site.register(Car)  # Регистрируем модель в админке
