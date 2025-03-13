# cars/urls.py
from django.urls import path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from . import views
from .views import home_view

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
    path('', home_view, name='home'),  # Открывать `index.html` на главной
    # Swagger URLs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # other URLs
    path('all/', views.get_all_cars, name='get_all_cars'),
    path('by_brand/<str:brand_query>/', views.get_cars_by_brand, name='get_cars_by_brand'),
    path('add/', views.add_car, name='add_car'),
    path('update/<int:car_id>/', views.update_car, name='update_car'),
    path('delete/<int:car_id>/', views.delete_car, name='delete_car'),
    path('<str:vin_number>/', views.get_car, name='get_car'),
]
