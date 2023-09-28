
from django.shortcuts import render, redirect
from user_onboarding.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import *
from django.contrib.auth import login, authenticate
from django.contrib import messages

#################################################
########### Register & Login ####################
#################################################
from django_ratelimit.decorators import ratelimit
from s2analytica.common import log_time, getratelimit

from s2analytica.common import getratelimit

@log_time
@ratelimit(key='ip', rate=getratelimit)
def user_login(request):
    # verified
    print("user_login")

    if request.user.is_authenticated:
        return redirect("/api/pms/v1/home/")  # change this to home page
    else:
        if request.method == "POST":
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            for_post = request.POST.get("for_post", "")
            
            # check if the user has entered for a post that the user is assigned to via django admin group
            if for_post:
                if User.objects.filter(username=username):
                    u_d = User.objects.get(username=username)
                    correct_group = u_d.groups.filter(name__in=[for_post]).exists()
                    if not correct_group:
                        messages.error(request, "Invalid post selection")
                        return redirect(request.path)

            if User.objects.filter(username=username):
                u_d = User.objects.get(username=username)
                user_password = u_d.check_password(password)
            else:
                user_password = False

            if User.objects.filter(username=username) and user_password == True:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    # return redirect("/user/trend_rating")
                    # change this to home page
                    return redirect("/api/pms/v1/home/")

                else:
                    messages.error(request, "Invalid username or password.")
                    return redirect(request.path)
            else:
                messages.error(request, "Invalid username or password.")
                return redirect(request.path)

    return render(request, "user_onboarding/login.html")

@log_time
@ratelimit(key='ip', rate=getratelimit)
def register_user(request):
    # verified

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
    return render(request, "user_onboarding/register.html")

@log_time
@login_required
@ratelimit(key='ip', rate=getratelimit)
def selector(request):
    return render(request, 'user_onboarding/selector.html')

#################################################
########### User Detail Section ####################
#################################################

@log_time
@login_required
@ratelimit(key='ip', rate=getratelimit)
def user_detail(request):
    user_detail = User.objects.get(username=request.user.id)
    context = {"u": user_detail}
    return render(request, "user_detail/user_profile.html", context)
