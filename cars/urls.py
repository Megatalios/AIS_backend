# cars/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('<str:vin_number>/', views.get_car, name='get_car'),
    path('by_brand/<str:brand_query>/', views.get_cars_by_brand, name='get_cars_by_brand'),
    path('add/', views.add_car, name='add_car'),
    path('update/<int:car_id>/', views.update_car, name='update_car'),
    path('delete/<int:car_id>/', views.delete_car, name='delete_car'),
]