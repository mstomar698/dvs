# views.py

import json
from django.http import JsonResponse
from django.db.models import Q
import random
from django.shortcuts import render
from rest_framework.decorators import api_view
from datetime import datetime
from pytz import timezone, utc

@api_view(['GET'])
def home(request):
    jsonData = {'message': 'Dashboard Home'}
    return JsonResponse(jsonData)

