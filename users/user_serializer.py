from rest_framework import serializers
import re
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для User с валидацией имени и email"""
    
    class Meta:
        model = User
        fields = ['name', 'email']

    def validate_name(self, value):
        """Валидация имени (только буквы и пробелы, от 2 до 100 символов)"""
        if not re.match(r'^[A-Za-zА-Яа-яЁё\s-]{2,100}$', value):
            raise serializers.ValidationError("Имя может содержать только буквы, пробелы и дефис (от 2 до 100 символов).")
        return value

    def validate_email(self, value):
        """Валидация email (проверка уникальности)"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже зарегистрирован.")
        return value
