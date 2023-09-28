
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
from models import Profile
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
# from app.domain.use_case.analytical_features.common_variable import *
from django_ratelimit.decorators import ratelimit

from s2analytica.common import log_time, getratelimit
#################################################
########### Register & Login ####################
#################################################


@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def user_login(request):
    if request.user.is_authenticated:
        return redirect("/cmm/sick_head_graph")
    else:
        if request.method == "POST":
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            if User.objects.filter(username=username):
                u_d = User.objects.get(username=username)
                user_password = u_d.check_password(password)
            else:
                user_password = False

            if User.objects.filter(username=username) and user_password == True:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("/cmm/sick_head_graph")
                else:
                    messages.error(request, "Invalid username or password.")
                    return redirect(request.path)
            else:
                messages.error(request, "Invalid username or password.")
                return redirect(request.path)

    return render(request, "login.html")


@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def register_user(request):
    if request.user.is_authenticated:
        return redirect("/login")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            email = request.POST.get("email", "")
            password = request.POST.get("password")
            re_password = request.POST.get("re-password")
            phone_number = request.POST.get("phonenumber", "")

            username_match = User.objects.filter(username=username)
            email_match = User.objects.filter(email=email)
            user_name_space = username.replace(" ", "")

            if len(user_name_space) == 0:
                messages.error(
                    request, "Please Enter Any Text in Username Field")
                return redirect(request.path)

            username_split = username.split(" ")
            if len(username_split) >= 2:
                messages.error(
                    request,
                    "Username Only Contains Alphanumeric Characters eg:-a-z, A-Z, 0-9(No Specials Character)",
                )
                return redirect(request.path)

            username_split_at_the_rate = username.split("@")
            if len(username_split_at_the_rate) >= 2:
                messages.error(
                    request,
                    "Username Only Contains Alphanumeric Characters eg:-a-z, A-Z, 0-9(No Specials Character)",
                )
                return redirect(request.path)

            username_split_excla = username.split("!")
            if len(username_split_excla) >= 2:
                messages.error(
                    request,
                    "Username Only Contains Alphanumeric Characters eg:-a-z, A-Z, 0-9(No Specials Character)",
                )
                return redirect(request.path)

            username_split_percentage = username.split("%")
            if len(username_split_percentage) >= 2:
                messages.error(
                    request,
                    "Username Only Contains Alphanumeric Characters eg:-a-z, A-Z, 0-9(No Specials Character)",
                )
                return redirect(request.path)

            username_split_and = username.split("&")
            if len(username_split_and) >= 2:
                messages.error(
                    request,
                    "Username Only Contains Alphanumeric Characters eg:-a-z, A-Z, 0-9(No Specials Character)",
                )
                return redirect(request.path)

            if username_match:
                messages.error(request, "Username Already Taken")
                return redirect(request.path)

            elif email_match:
                messages.error(request, "Email Already Taken")
                return redirect(request.path)

            elif password != re_password:
                messages.error(request, "Password Do not Match!")
                return redirect(request.path)
            else:
                u_name = username.split(" ")
                if len(u_name) >= 2:
                    first_name = u_name[0]
                    last_name = u_name[1]
                else:
                    first_name = u_name[0]
                    last_name = " "
                user_detail = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                    email=email,
                )

                user_detail.save()
                user = User.objects.get(username=user_detail.username)
                messages.success(
                    request, "You are Successfully Register, Please Login")
                return redirect("/login")
    return render(request, "register.html")


#################################################
########### User Detail Section ####################
#################################################


@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
def user_detail(request):
    user_detail = Profile.objects.get(username=request.user.id)
    context = {"u": user_detail}
    return render(request, "user_detail/user_profile.html", context)
