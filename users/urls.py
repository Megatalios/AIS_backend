from django.urls import path
from . import views

urlpatterns = [
    path('<int:user_id>/', views.get_user, name='get_user'),
    path('all/', views.get_all_users, name='get_all_users'),
    path('add/', views.add_user, name='add_user'),
    path('update/<int:user_id>/', views.update_user, name='update_user'),
    path('delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('by_name/<str:name_query>/', views.get_users_by_name, name='get_users_by_name'),
]