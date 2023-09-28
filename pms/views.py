# views.py

import json

from django.http import HttpResponse
from .serializers import DataSerializer
from .models import Data
from django.db.models import Q
import random
from django.shortcuts import render
from rest_framework import viewsets
from .models import Sensor, Device, Data
from .serializers import SensorSerializer, DeviceSerializer, DataSerializer, DataCreateSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Device, Sensor
from .serializers import DeviceSerializer, SensorSerializer
from datetime import datetime
from pytz import timezone, utc


@api_view(['POST'])
def create_device(request):
    serializer = DeviceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_sensor(request):
    serializer = SensorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_data(request):
    serializer = DataCreateSerializer(data=request.data)
    if serializer is not None and serializer.is_valid():
        uname = serializer.validated_data['uname']  # type: ignore
        passw = serializer.validated_data['passw']  # type: ignore
        sensor_name = serializer.validated_data['sensor_name']  # type: ignore
        value = serializer.validated_data['value']  # type: ignore
        try:
            device = Device.objects.get(uname=uname, passw=passw)
            print("device found")
        except Device.DoesNotExist:
            print("device not found")
            return Response({'error': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            sensor = Sensor.objects.get(name=sensor_name)
            print("sensor found")
        except Sensor.DoesNotExist:
            return Response({'error': 'Sensor not found'}, status=status.HTTP_404_NOT_FOUND)
        data = Data(device=device, sensor=sensor, data=value)
        data.save()

        return Response({'message': 'Data created successfully'}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_sensors(request):
    all_sensors = Sensor.objects.all()
    all_devices = Device.objects.all()
    available_devices = []
    available_sensors = []
    for sensor in all_sensors:
        available_sensors.append(sensor.name)
    for device in all_devices:
        if str(request.user.username) == device.username:
            available_devices.append(device.uname)

    sensor_name = request.GET.get('sensor_name')
    # Set date here
    start_date = request.GET.get('start_date')
    start_time = request.GET.get('start_time')
    end_date = request.GET.get('end_date')
    end_time = request.GET.get('end_time')
    # print(f"start date: {start_date}, start time: {start_time}, end date: {end_date}, end time: {end_time}")
    start_datetime_ist = datetime.strptime(f"{start_date} {start_time}", '%Y-%m-%d %H:%M')
    end_datetime_ist = datetime.strptime(f"{end_date} {end_time}", '%Y-%m-%d %H:%M')
    indian_timezone = timezone('Asia/Kolkata')
    start_datetime_utc = indian_timezone.localize(start_datetime_ist).astimezone(utc)
    end_datetime_utc = indian_timezone.localize(end_datetime_ist).astimezone(utc)
    # date end

    if sensor_name is None:
        return render(request, 'pms/home.html', {'sensors': available_sensors, 'devices': available_devices, 'message': 'Provide a valid sensor name'})
    else:
        clicked_sensor = Sensor.objects.filter(name=sensor_name)
        if not clicked_sensor:
            return render(request, 'pms/home.html', {'sensors': available_sensors, 'devices': available_devices, 'message': 'Provide a valid sensor name'})
        for sensor in clicked_sensor:
            # print(f"sensor for which table is to be created is {sensor}")
            data = Data.objects.filter(sensor_id=sensor.id)
            
        if end_datetime_utc:
            data = data.filter(created_at__gte=start_datetime_utc,
                            created_at__lt=end_datetime_utc)
            # print(f" the data afeter filtering for date is {data} between {start_datetime_utc} and {end_datetime_utc}")

        serializer = DataSerializer(data, many=True)

        for entry in serializer.data:
            created_at_str = entry['created_at']
            created_at_datetime = datetime.fromisoformat(created_at_str)
            entry['formatted_created_at'] = created_at_datetime.strftime("%Y-%m-%d %I:%M %p")
            device_id = entry['device']
            device = Device.objects.get(id=device_id)
            entry['device'] = device.uname


        return render(request, 'pms/sensors.html', {'sensor': sensor, 'filtered_data': serializer.data, 'start_date': start_date, 'start_time': start_time, 'end_date': end_date, 'end_time': end_time})

@api_view(['GET'])
def get_devices(request):
    devices = Device.objects.all()
    serializer = DeviceSerializer(devices, many=True)
    print(serializer.data)
    return render(request, 'pms/devices.html', {'sensors': serializer.data})


@api_view(['POST'])
def get_data(request):
    data = Data.objects.all()
    all_sensors = Sensor.objects.all()
    all_devices = Device.objects.all()
    # Set date here
    start_date = request.data.get('start_date')
    start_time = request.data.get('start_time')
    end_date = request.data.get('end_date')
    end_time = request.data.get('end_time')

    start_datetime_ist = datetime.strptime(f"{start_date} {start_time}", '%Y-%m-%d %H:%M')
    end_datetime_ist = datetime.strptime(f"{end_date} {end_time}", '%Y-%m-%d %H:%M')
    indian_timezone = timezone('Asia/Kolkata')
    start_datetime_utc = indian_timezone.localize(start_datetime_ist).astimezone(utc)
    end_datetime_utc = indian_timezone.localize(end_datetime_ist).astimezone(utc)
    # date end
    sensor_type = request.data.get('sensor-dropdown')
    device_number = request.data.get('device-dropdown')
    sensors_by_id = {}
    devices_by_id = {}
    available_devices = []
    available_sensors = []
    for sensor in all_sensors:
        sensors_by_id[sensor.id] = sensor.name
        available_sensors.append(sensor.name)
    for device in all_devices:
        devices_by_id[device.id] = device.uname
        if str(request.user.username) == device.username: #device.uname
            available_devices.append(device.uname)

    if device_number == '' or sensor_type == '':
        print("no device or sensor selected")
        return render(request, 'pms/home.html', {'available_devices': available_devices, 'available_sensors': available_sensors, 'message': 'Please select a device and sensor'})
    
    selected_sensors = [sensor.strip() for sensor in sensor_type.split(',')]
    selected_devices = [device.strip() for device in device_number.split(',')]
    # print(f"sensor_type: {selected_sensors} && {type(selected_sensors)}, device_number: {selected_devices} && {type(selected_devices)}, date: {start_date} -> {end_date}")
    if selected_sensors:
        sensor_ids = Sensor.objects.filter(
            name__in=selected_sensors).values_list('id', flat=True)
        # print(f"sensor ids are {sensor_ids}")
        data = data.filter(sensor_id__in=sensor_ids)
        # print(f" the data afeter filtering for sensors is {data}")

    if selected_devices:
        devices_ids = Device.objects.filter(
            uname__in=selected_devices).values_list('id', flat=True)
        # print(f"device ids are {devices_ids}")
        data = data.filter(device_id__in=devices_ids)
        # print(f" the data afeter filtering for devices is {data}")
    

    if end_datetime_utc:
        data = data.filter(created_at__gte=start_datetime_utc,
                           created_at__lt=end_datetime_utc)
        # print(f" the data afeter filtering for date is {data} between {start_datetime_utc} and {end_datetime_utc}")

    serializer = DataSerializer(data, many=True)

    filtered_data = json.dumps(serializer.data)

    context = {
        'filtered_data': filtered_data,
        'sensor_type': sensor_type,
        'device_number': device_number,
        'provided_satrt_date': start_date,
        'provided_end_date': end_date,
        'provided_start_time': start_time,
        'provided_end_time': end_time, 
        'sensors_by_id': sensors_by_id,
        'devices_by_id': devices_by_id,
        'available_devices': available_devices,
        'available_sensors': available_sensors,
    }
    return render(request, 'pms/data.html', context)


@api_view(['GET'])
def home(request):
    all_sensors = Sensor.objects.all()
    all_devices = Device.objects.all()
    available_devices = []
    available_sensors = []
    for sensor in all_sensors:
        available_sensors.append(sensor.name)
    for device in all_devices:
        if str(request.user.username) == device.username:
            available_devices.append(device.uname)
    return render(request, 'pms/home.html', {'available_devices': available_devices, 'available_sensors': available_sensors})


@api_view(['POST'])
def get_pie_chart_data(request):
    all_sensors = Sensor.objects.all()
    all_devices = Device.objects.all()
    all_data = Data.objects.all()
    sensor_label = []
    color_label = []
    device_label = []
    data_label = []
    pie_chart_data = {}
    sensor_data = {}

    for sensor in all_sensors:
        # print(f"sensor name: {sensor.name}")
        sensor_label.append(sensor.name)
        random_color = "#{:02x}{:02x}{:02x}".format(random.randint(
            0, 255), random.randint(0, 255), random.randint(0, 255))
        color_label.append(random_color)
        sensor_data[sensor.name] = []

    for devices in all_devices:
        if str(request.user.username) == devices.username:
            # print(f"device name for current user: {devices.name}")
            device_label.append(devices.name)
    new_data = []
    for data in all_data:
        new_data.append(data.data)
        if str(request.user.username) == data.device.username:
            sensor_data[str(data.sensor)].append(data.data)
        else:
            sensor_data[str(data.sensor)].append(0)


    if not (color_label or sensor_label or device_label or sensor_data):
        print("No data found, dummy data is being sent")
        color_label = ["red", "blue", "green"]
        sensor_label = ["tds", "temperature", "humidity"]
        device_label = ["d1", "d2", "d3"]
        data_label = [30, 40, 50]
        pie_chart_data = {
            "sensors": sensor_label,
            "data": data_label,
            "backgroundColor": color_label,
            "devices": device_label,
        }
    else:
        data_label = [sum(sensor_data[sensor]) / len(sensor_data[sensor])
                      if sensor_data[sensor] else 0 for sensor in sensor_label]
        # print(f"average data: {data_label} for sensor: {all_sensors} with all devices: {all_devices} and current user is {request.user.username}")
        pie_chart_data = {
            "sensors": sensor_label,
            "backgroundColor": color_label,
            "data": new_data[:100],
            "devices": device_label,
        }

    return Response(pie_chart_data)
