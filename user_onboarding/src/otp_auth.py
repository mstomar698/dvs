
import json
from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
import requests
from s2analytica.common import log_time, getratelimit

from s2analytica.settings import AUTH

from ..models import *
from django.contrib.auth.models import *
from django_ratelimit.decorators import ratelimit

api_key = AUTH["api_key"]



def send_otp_request(to):
    number = "+91"+to
    url = f"https://2factor.in/API/V1/{api_key}/SMS/{number}/AUTOGEN/OTP1"

    response = requests.get(url)
    data = response.json()

    if data["Status"] == "Success":
        session_id = data["Details"]
        return session_id
    else:
        return None


@ratelimit(key='ip', rate='10/m')
def verify_otp(session_id, otp_code):
    url = f"https://2factor.in/API/V1/{api_key}/SMS/VERIFY/{session_id}/{otp_code}"

    response = requests.get(url)
    data = response.json()

    if data["Status"] == "Success":
        if data["Details"] == "OTP Matched":
            return True
        else:
            return False
    else:
        return False

@log_time
@ratelimit(key='ip', rate=getratelimit)
def otp_auth(request):
    messages = []
    return render(request, "user_onboarding/otp_auth.html", {'messages': messages})

@log_time
@ratelimit(key='ip', rate=getratelimit)
def otp_val(request):
    if request.method == 'POST':
        to = request.POST.get('phone')
        print(f"Phone Number: {to}")
        phone_number = PhoneNumber.objects.filter(mobile_number=to).first()

        if phone_number is None:
            messages = []
            messages.append("Phone Number does not exist in our database")
            print(messages)
            return render(request, 'user_onboarding/otp_auth.html', {'messages': messages})

        user = phone_number.user
        print(f"Linked User: {user}")

        messages = []
        print("otp sent proceed to next step")
        session_id = send_otp_request(to)

        if session_id:
            print(f"OTP request sent successfully. Session ID: {session_id}")
        else:
            print("Failed to send OTP request. Please check your API key and number.")
        if session_id:
            print(f"OTP request sent successfully. Session ID: {session_id}")
            request.session['phone_number'] = to
            request.session['session_id'] = session_id
            messages.append(
                "OTP request sent successfully. Please check your phone.")
            return render(request, 'user_onboarding/otp.html', {'messages': messages})
        else:
            error_message = "Failed to send OTP request. Please check your API key and number."
            messages.append(error_message)
            return render(request, 'user_onboarding/otp_auth.html', {'messages': messages})

    messages = []
    messages.append("Invalid Request")
    return render(request, 'user_onboarding/otp_auth.html', {'messages': messages})

@log_time
@ratelimit(key='ip', rate=getratelimit)
def otp_confirm(request):
    if request.method == 'POST':
        otp_code = request.POST.get('OTP')
        session_id = request.session.get('session_id')
        print(f"OTP code: {otp_code}")
        print(f"Session ID: {session_id}")
        messages = []
        try:
            if session_id and otp_code:
                is_otp_correct = verify_otp(session_id, otp_code)

                if is_otp_correct:
                    to = request.session.get('phone_number')
                    phone_number = PhoneNumber.objects.filter(
                        mobile_number=to).first()

                    if phone_number is None:
                        messages = []
                        messages.append(
                            "Phone Number does not exist in our database")
                        print(messages)
                        return render(request, 'user_onboarding/otp_auth.html', {'messages': messages})

                    user = phone_number.user

                    if User.objects.filter(username=user.user_name):
                        u_d = User.objects.get(username=user.user_name)
                        if u_d:
                            print(f"logging in for {u_d}")
                            login(request, u_d)
                            return redirect("/api/pms/v1/home/")
                        else:
                            error_message = "Authentication failed, please try again"
                            messages.append(error_message)
                            return render(request, 'user_onboarding/otp.html', {'messages': messages})
                    else:
                        error_message = "User not found"
                        messages.append(error_message)
                        return render(request, 'user_onboarding/otp_auth.html', {'messages': messages})
                else:
                    error_message = "Invalid code"
                    messages.append(error_message)
                    return render(request, 'user_onboarding/otp.html', {'messages': messages})
            else:
                error_message = "Missing session ID or OTP code"
                messages.append(error_message)
                return render(request, 'user_onboarding/otp.html', {'messages': messages})

        except Exception as e:
            error_message = "An error occurred: " + str(e)
            messages.append(error_message)
            return render(request, 'user_onboarding/otp.html', {'messages': messages})

    messages.append("Invalid Request")
    return render(request, 'user_onboarding/otp_auth.html', {'messages': messages})

@log_time
@ratelimit(key='ip', rate=getratelimit)
def phone_otp_send(request):
    if request.method == "POST":
        registration_data = json.loads(request.COOKIES.get(
            'registration_data_to_validate', '{}'))
        phone = registration_data.get('phone', '')
        print(f"Phone Number: {phone}")
        phone_number = PhoneNumber.objects.filter(mobile_number=phone).first()
        if phone_number:
            messages = []
            messages.append("Phone Number already registered")
            print(messages)
            return JsonResponse({'message': 'Number already registered'})
        session_id = send_otp_request(phone)
        messages = []
        if session_id:
            print(f"OTP request sent successfully. Session ID: {session_id}")
            request.session['phone_number'] = phone
            request.session['session_id'] = session_id
            messages.append(
                "OTP request sent successfully. Please check your phone.")
            return JsonResponse({'message': 'OTP request sent successfully. Please check your phone.'})
        else:
            error_message = "Failed to send OTP request. Please check your API key and number."
            messages.append(error_message)
            return JsonResponse({'message': 'OTP Failed to send'})

    return JsonResponse({'message': 'Invalid request method'})

@log_time
@ratelimit(key='ip', rate=getratelimit)
def phone_otp_val(request):
    if request.method == "POST":
        registration_data = json.loads(request.COOKIES.get(
            'registration_data_to_validate', '{}'))
        phone_otp = registration_data.get('phone_otp', '')
        session_id = request.session.get('session_id')
        print(f"Session ID: {session_id}")
        print(f"Phone OTP: {phone_otp}")
        if session_id and phone_otp:
            is_otp_correct = verify_otp(session_id, phone_otp)
            if is_otp_correct:
                print("phone_otp_val")
                request.session['phone_otp_registration_ver'] = True
                return JsonResponse({'message': 'OTP Verified'})
            else:
                request.session['phone_otp_registration_ver'] = False
                return JsonResponse({'message': 'Incorrect OTP'})

        else:
            return JsonResponse({'message': 'Invalid request method'})
