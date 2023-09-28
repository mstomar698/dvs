from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import smtplib
from django.http import JsonResponse
from django.conf import settings
from random import randint
from s2analytica.settings import EMAIL_HOST_PASSWORD, EMAIL_HOST_USER
from django.contrib.auth.models import User
from django_ratelimit.decorators import ratelimit
from s2analytica.common import log_time, getratelimit
from datetime import datetime
import time

email_host = EMAIL_HOST_USER
email_host_password = EMAIL_HOST_PASSWORD


def send_email(subject, body, to_email):
    
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login(email_host, email_host_password)

    message = MIMEMultipart()
    message['From'] = email_host
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    smtpObj.sendmail(email_host, to_email, message.as_string())
    smtpObj.quit()

@log_time
@ratelimit(key='ip', rate=getratelimit)
def email_otp_send(request):
    global ts
    ts=int(time.time())
    if request.method == "POST":
        registration_data = json.loads(request.COOKIES.get(
            'registration_data_to_validate', '{}'))
        email = registration_data.get('email', '')
        user_email = User.objects.filter(email=email)
        if user_email:
            messages = []
            messages.append("Email already registered")
            print(messages)
            return JsonResponse({'message': 'Email already registered'})

        otp = randint(100000, 999999)

        try:
            subject = 'Email Verification'
            body = f'Hello Sir, \
                    Your OTP is: {otp} for registration of {email}. \
                    By: Sarva Suvidhaen Pvt Ltd \
                    Regards,'
            send_email(subject, body, email)
            
            print(f"*****email sent for user: {email}")
            
        except Exception as e:
            print(f"*****Exception for the mail: {str(e)}")

        request.session['otp'] = otp
        return JsonResponse({'message': 'Email sent successfully, Please check your Email.'})

    return JsonResponse({'message': 'Invalid request method'})

@ratelimit(key='ip', rate='20/m')
def email_otp_val(request):
    if request.method == "POST":

        registration_data = json.loads(request.COOKIES.get(
            'registration_data_to_validate', '{}'))
        user_otp = registration_data.get('otp', '')
        otp = request.session.get('otp')
        if (len(user_otp) < 6):
            return JsonResponse({'message': 'OTP length should be 6'})
        if otp == int(user_otp):
            request.session['email_otp_registration_ver'] = True

            expiration_time = ts + 60*30
            response_data={'message':'OTP Varified'}
            response = JsonResponse(response_data)
            response['X-Timestamp'] = expiration_time

            return response

        else:
            request.session['email_otp_registration_ver'] = False
            return JsonResponse({'message': 'Incorrect OTP'})

    return JsonResponse({'message': 'Invalid request method'})
