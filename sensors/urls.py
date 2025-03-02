# sensors/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('<int:sensor_data_id>/', views.get_sensor_data, name='get_sensor_data'),
    path('car/<str:car_vin>/', views.get_sensor_data_for_car, name='get_sensor_data_for_car'),
    path('add/', views.add_sensor_data_record, name='add_sensor_data_record'),
    path('update/<int:sensor_data_id>/', views.update_sensor_data_record, name='update_sensor_data_record'),
    path('delete/<int:sensor_data_id>/', views.delete_sensor_data_record, name='delete_sensor_data_record'),
    # ... (возможно, другие URL-пути) ...
]