from django.shortcuts import render
from django.http import JsonResponse
from .models import User  # Импорт модели User из users.models
from django.views.decorators.csrf import csrf_exempt
import json

# Получить пользователя по ID
def get_user(request, user_id):
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
    
# Получить пользователя по имени
def get_users_by_name(request, name_query):
    users = User.objects.filter(name__icontains=name_query) # __icontains - регистронезависимое "содержит"
    users_data = []
    for user in users:
        users_data.append({
            'id': user.id,
            'name': user.name,
            'email': user.email
        })
    return JsonResponse({'users': users_data}) # Возвращаем список пользователей в JSON

# Получить всех пользователей (вряд ли пригодится, но для проверки - мб)
def get_all_users(request):
    all_users = User.objects.all()
    users_list = []
    for user in all_users:
        users_list.append({'id': user.id, 'name': user.name, 'email': user.email})
    return JsonResponse({'users': users_list})

# CSRF защита (в реальных проектах не использовать)
@csrf_exempt
def add_user(request):
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
    
# CSRF защита (в реальных проектах не использовать)
@csrf_exempt
def update_user(request, user_id): # user_id передается в URL
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


# CSRF защита (в реальных проектах не использовать)
@csrf_exempt
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
