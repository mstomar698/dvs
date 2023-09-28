from django.urls import path
# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# router = DefaultRouter()
# router.register(r'sensors', views.SensorViewSet)
# router.register(r'devices', views.DeviceViewSet)
# router.register(r'data', views.DataViewset)

urlpatterns = [
    # Create data APIs
    path('create-sensor/', views.create_sensor, name='create-sensor'),
    path('create-device/', views.create_device, name='create-device'),
    path('create-data/', views.create_data, name='create-data'),
    # Get data APIs
    path('get-sensors/', views.get_sensors, name='get-sensors'),
    path('get-devices/', views.get_devices, name='get-devices'),
    path('get-data/', views.get_data, name='get-data'),
    path('get-pie-chart-data/', views.get_pie_chart_data, name='get-pie-chart-data'),
    path('home/', views.home, name='home'),
]