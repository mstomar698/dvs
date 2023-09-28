
from django.shortcuts import render, redirect
from s2analytica.common import log_time, getratelimit
from user_onboarding.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django_ratelimit.decorators import ratelimit
from django.contrib.auth.hashers import make_password, check_password

@log_time
@ratelimit(key='ip', rate=getratelimit)
def request_user(request):
    # verified

    if request.user.is_authenticated:
        return redirect("/auth/login")
    else:
        if request.method == "POST":
            username = request.POST.get("username", '')
            email = request.POST.get("email", "")
            phone_number = request.POST.get("phone", "")
            password = request.POST.get("password")
            re_password = request.POST.get("re-password")
            for_post = request.POST.get('for_post','')

            username_match = User.objects.filter(username=username)
            email_match = User.objects.filter(email=email)

            if username_match:
                messages.error(request, "Username Already Exists")
                return redirect(request.path)
            if email_match:
                messages.error(request, "Email Already Exists")
                return redirect(request.path)
            
            phoneNumber_match = PhoneNumber.objects.filter(mobile_number=phone_number)
            if len(phoneNumber_match) > 0:
                messages.error(request, "Phone Number Already Exists")
                return redirect(request.path)


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

            # if username_match:
            #     messages.error(request, "Username Already Taken")
            #     return redirect(request.path)

            # elif email_match:
            #     messages.error(request, "Email Already Taken")
            #     return redirect(request.path)

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

                phone = PhoneNumber.objects.create(
                    user=user_detail,
                    mobile_number=phone_number
                )

                phone.save()

                user_id = user_detail.id
                print(f"User ID: {user_id}")
                print(f"User phone details and linked user: {phone}")
                print(f"User phone details and linked user: {phone.user}")

                messages.success(
                    request, "You are Successfully Reuqested for User, Please Wait For Some Time")
                return redirect("/auth/login")
    return render(request, 'user_onboarding/request_user.html')


@login_required
@ratelimit(key='ip', rate=getratelimit)
def show_requested_user(request):
    # verified

    current_user = User.objects.get(id=request.user.id)
    if current_user.groups.filter(name="Railway Admin").exists():
        user_requested = Request_User.objects.filter(seen=False)
        context = {'user_requested': user_requested}
        return render(request, 'user_onboarding/requested_user.html', context)
    else:
        messages.error(request, 'You do not Have Access to It!')
        return redirect('../../railmadad/trend_rating/', permanent=True)


@login_required
@ratelimit(key='ip', rate=getratelimit)
def requested_user(request, user_id, arg):
    # verified

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
                return redirect('/auth/show_user_requested/')

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
                return redirect('/auth/show_user_requested/')
            else:
                messages.success(request, 'Deny The User')
                return redirect('/auth/show_user_requested/')
        else:
            messages.error(request, 'You do not Have Access to It!')
            return redirect('/api/pms/v1/home/')
    else:
        messages.error(request, 'Something Went Wrong')
        return redirect('/api/pms/v1/home/')
