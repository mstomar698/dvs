

from ast import Div
from email import message
from pickle import NONE
from pydoc import resolve
from sre_parse import CATEGORIES
from tracemalloc import start
import operator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from pip import main
from app.models import *
import dateutil.parser
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth import login as auth_login
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.models import *
from django.db.models import Count
from operator import itemgetter
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from email.mime.image import MIMEImage
import os
import datetime
from datetime import datetime as dt
import calendar
from django.db.models import Sum
import csv
import json
from datetime import date, timedelta, datetime
from dateutil.rrule import rrule, MONTHLY
import calendar
from calendar import monthrange
import datetime as DT
from railway.settings import BASE_DIR
import os
import time
import urllib
from django.db.models import Sum
# from app.domain.use_cases.analytical_features.common_variable import *
from django_ratelimit.decorators import ratelimit

from s2analytica.common import log_time, getratelimit

@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def edit_profile(request):
    user_detail = Profile.objects.get(username=request.user.id)
    user_d = User.objects.get(id=request.user.id)
    if request.method == "POST":
        username = request.POST.get("username", "")
        phone_number = request.POST.get("phone", "")
        email = request.POST.get("email", "")

        user_d.username = username
        user_detail.phone_number = phone_number
        user_detail.email = email
        user_detail.save()
        messages.success(request, "Successfully Edited")
        return redirect("/auth/user_profile")
    context = {"u": user_detail}
    return render(request, "user_detail/edit_profile.html", context)


@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def user_profile(request):
    user = User.objects.get(id=request.user.id)
    context = {"user": user}
    return render(request, "user_profile.html", context)


@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def change_password(request):
    if request.method == "POST":
        current_password = request.POST.get("c-password", "")
        future_password = request.POST.get("f-password", "")
        user = User.objects.get(id=request.user.id)
        user_password = user.check_password(current_password)
        if user_password:
            user.set_password(future_password)
            user.save()
            messages.success(
                request, "You Have Successfully Changed Your Password")
            return redirect(request.path)
        else:
            messages.error(
                request, "You Current Password is Wrong, Please Try Again")
            return redirect(request.path)
    context = {}
    return render(request, "change_password.html", context)
