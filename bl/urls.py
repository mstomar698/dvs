
# urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Create data APIs
    # Get data APIs
    path('home/', views.home, name='home'),
]