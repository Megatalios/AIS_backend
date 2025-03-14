# sensors/urls.py
from django.urls import path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from . import views

schema_view = get_schema_view(
    openapi.Info(
        title="Car digital twin API",
        default_version='v1',
        description="Car digital twin API",
        # terms_of_service="https://example.com",
        # contact=openapi.Contact(email="contact@mail.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Swagger URLs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('save-sensor-data/', views.save_sensor_data, name='save_sensor_data'),
     # other URLs
    path('all/', views.get_all_sensors, name='get_all_sensors'),
    path('add/', views.add_sensor_data_record, name='add_sensor_data_record'),
    path('check/', views.check_sensor_data, name='check_sensor_data'),
    path('get_user_info/', views.get_user_info, name='get_user_info'),
    path('<int:sensor_data_id>/', views.get_sensor_data, name='get_sensor_data'),
    path('<str:car_vin>/', views.get_sensor_data_for_car, name='get_sensor_data_for_car'),
    path('update/<int:sensor_data_id>/', views.update_sensor_data_record, name='update_sensor_data_record'),
    path('delete/<int:sensor_data_id>/', views.delete_sensor_data_record, name='delete_sensor_data_record'),
    path('calculate/<int:sensor_data_id>/', views.get_result_processing, name='get_result_processing'),
    path('calculate/save/<int:sensor_data_id>/', views.save_calculated_sensor_data, name='save_calculated_sensor_data'),
    
    # ... (возможно, другие URL-пути) ...
]