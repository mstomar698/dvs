# views.py

import json

from django.http import HttpResponse
from django.db.models import Q
import random
from django.shortcuts import render
from rest_framework import viewsets

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from pytz import timezone, utc


@api_view(['GET'])
def home(request):
    return render(request, 'bl/home.html', {'message': 'DashBoard Home'})

