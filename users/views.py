from django.shortcuts import render
from django.http import JsonResponse
from .models import User
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework import serializers
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from .forms import RegisterForm



@api_view(['GET'])
def get_user(request, user_id):
    """Получить пользователя по ID"""
    try:
        user = User.objects.get(id=user_id)
        user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email
        }
        return JsonResponse(user_data)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
@api_view(['GET'])
def get_users_by_name(request, name_query):
    """Получить пользователей по имени"""
    users = User.objects.filter(name__icontains=name_query) # __icontains - регистронезависимое "содержит"
    users_data = []
    for user in users:
        users_data.append({
            'id': user.id,
            'name': user.name,
            'email': user.email
        })
    return JsonResponse({'users': users_data}) # Возвращаем список пользователей в JSON

@api_view(['GET'])
def get_all_users(request):
    """Получить всех пользователей"""
    all_users = User.objects.all()
    users_list = []
    for user in all_users:
        users_list.append({'id': user.id, 'name': user.name, 'email': user.email})
    return JsonResponse({'users': users_list})

# Сериализатор для описания тела запроса
class UserSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()

# @swagger_auto_schema(
#     method='POST',
#     request_body=UserSerializer,  # Указываем сериализатор для тела запроса
#     responses={200: 'User registered successfully'}
# )
# @api_view(['POST'])
def register_view(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect('/')  # Укажите вашу главную страницу
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

def logout_view(request):
    logout(request)
    return redirect('home')


@swagger_auto_schema(
    method='POST',
    request_body=UserSerializer,  # Указываем сериализатор для тела запроса
    responses={200: 'Car added successfully'}
)
@api_view(['POST'])
def add_user(request):
    """Добавить пользователя"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body) # Читаем JSON из тела запроса
            name = data.get('name')
            email = data.get('email')

            if not name or not email:
                return JsonResponse({'error': 'Name and email are required'}, status=400)

            user = User(name=name, email=email)
            user.save() # Сохраняем пользователя в базу данных
            return JsonResponse({'message': 'User created successfully', 'user_id': user.id}, status=201) # 201 Created status
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST method allowed'}, status=405) # 405 Method Not Allowed



@swagger_auto_schema(
    method='PUT',
    request_body=UserSerializer,  # Указываем сериализатор для тела запроса
    responses={200: 'Car updated successfully'}
)    
@api_view(['PUT'])
def update_user(request, user_id): # user_id передается в URL
    """Обновить пользователя"""
    if request.method == 'PUT': # Используем PUT для обновления
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')

            try:
                user = User.objects.get(id=user_id) # Находим пользователя по ID
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

            if name: # Обновляем только если переданы новые значения
                user.name = name
            if email:
                user.email = email
            user.save() # Сохраняем изменения
            return JsonResponse({'message': 'User updated successfully', 'user_id': user.id})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Only PUT method allowed'}, status=405)


@api_view(['DELETE'])
def delete_user(request, user_id): # user_id в URL
    if request.method == 'DELETE': # Используем DELETE метод
        try:
            user = User.objects.get(id=user_id)
            user.delete() # Удаляем пользователя
            return JsonResponse({'message': 'User deleted successfully', 'user_id': user_id})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    else:
        return JsonResponse({'error': 'Only DELETE method allowed'}, status=405)
