# serializers.py

from rest_framework import serializers
from .models import Sensor, Device, Data

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = '__all__'



class DataCreateSerializer(serializers.Serializer):
    uname = serializers.CharField(max_length=1000)
    passw = serializers.CharField(max_length=1000)
    sensor_name = serializers.CharField(max_length=1000)
    value = serializers.FloatField()
    # values = serializers.ListField(
    #     child=serializers.DictField(
    #         child=serializers.CharField(max_length=50)
    #     )
    # )
    