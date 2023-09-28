from ast import Div
from email import message
from pickle import NONE
from pydoc import resolve
from sre_parse import CATEGORIES
from tracemalloc import start
import operator
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from pip import main
from django.contrib.auth.models import Group
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
from app.models import *
from django_ratelimit.decorators import ratelimit


def request_user(request):
    if request.user.is_authenticated:
        return redirect("/login")
    else:
        if request.method == "POST":
            username = request.POST.get("username", '')
            email = request.POST.get("email", "")
            password = request.POST.get("password")
            re_password = request.POST.get("re-password")
            for_post = request.POST.get('for_post', '')

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
                user_detail = Request_User(
                    user_name=username,
                    user_password=password,
                    user_email=email,
                    for_post=for_post
                )

                user_detail.save()
                messages.success(
                    request, "You are Successfully Reuqested for User, Please Wait For Some Time")
                return redirect("/login")
    return render(request, 'request_user.html')


@login_required
@ratelimit(key='ip', rate=getratelimit)
def show_requested_user(request):
    current_user = User.objects.get(id=request.user.id)
    if current_user.groups.filter(name="Railway Admin").exists():
        user_requested = Request_User.objects.filter(seen=False)
        context = {'user_requested': user_requested}
        return render(request, 'requested_user.html', context)
    else:
        messages.error(request, 'You do not Have Access to It!')
        return redirect('/cmm/sick_head_graph/')


@login_required
@ratelimit(key='ip', rate=getratelimit)
def requested_user(request, user_id, arg):
    print(request.method)
    if request.method == "POST":
        current_user = User.objects.get(id=request.user.id)
        if current_user.groups.filter(name="Railway Admin").exists():

            if arg == "APPROVE":
                approved = True
            else:
                approved = False

            if Request_User.objects.filter(id=user_id):
                user = Request_User.objects.get(id=user_id)
            else:
                messages.error(request, 'User Does Not Exists')
                return redirect('/cmm/show_user_requested/')

            user.seen = True
            user.save()

            if approved:
                user.approved = True
                user.save()
                password = make_password(f"{user.user_password}")
                create_user = User(
                    username=user.user_name,
                    email=user.user_email,
                    password=password,
                )
                create_user.save()

                if user.for_post == "Moderator":
                    if Group.objects.filter(name='Moderator'):
                        my_group = Group.objects.get(name='Moderator')
                    else:
                        my_group = Group(name="Moderator")
                        my_group.save()
                    create_user.groups.add(my_group)

                # elif user.for_post == "Superuser":
                #     create_user.is_staff = True
                #     create_user.is_superuser = True
                #     create_user.is_admin = True
                #     create_user.save()
                #     moderator_group = Group.objects.get(name='Moderator')
                #     create_user.groups.add(moderator_group)

                elif user.for_post == "Railway Admin":
                    if Group.objects.filter(name='Railway Admin'):
                        my_group = Group.objects.get(name='Railway Admin')
                    else:
                        my_group = Group(name="Railway Admin")
                        my_group.save()

                    moderator_group = Group.objects.get(name='Moderator')
                    create_user.groups.add(moderator_group)
                    create_user.groups.add(my_group)

                elif user.for_post == "Normal User":
                    pass

                create_user.save()
                messages.success(request, 'Approved The User')
                return redirect('/cmm/show_user_requested/')
            else:
                messages.success(request, 'Deny The User')
                return redirect('/cmm/show_user_requested/')
        else:
            messages.error(request, 'You do not Have Access to It!')
            return redirect('/cmm/sick_head_graph/')
    else:
        messages.error(request, 'Something Went Wrong')
        return redirect('/cmm/sick_head_graph/')
