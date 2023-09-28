from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
# from user.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from .user_form import PasswordResetConfirmForm
from s2analytica.common import log_time, getratelimit

from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.conf import settings


User = get_user_model()
from django_ratelimit.decorators import ratelimit

@log_time
@ratelimit(key='ip', rate=getratelimit)
def password_reset_request(request):
    # verified

    if request.method == "POST":
        data = request.POST.get('email')
        if data is not None:

            user = User.objects.filter(Q(email=data)).first()
            if user is not None:
                subject = "Password Reset Requested"
                email_template_name = "user_onboarding/password_reset_email.txt"
                c = {
                    "email": user.email,
                    # 'domain':'localhost:8000',
                    'domain': 's2analytica.suvidhaen.org',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    # 'protocol': 'http',
                    'protocol': 'https',
                }
                email = render_to_string(email_template_name, c)
                try:
                    send_mail(subject, email, settings.EMAIL_HOST_USER, [
                              user.email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')

                return redirect("/auth/password_reset/done/")
            else:
                messages.error(request, 'Email is not registered')
                return redirect("/auth/forget_password")
        else:
            messages.error(request, 'Please enter the Email')
            return redirect("/auth/forget_password")

    return render(request, 'user_onboarding/password_reset.html')

@log_time
@ratelimit(key='ip', rate=getratelimit)
def PasswordResetConfirmView(request, uidb64=None, token=None):
    # verified

    assert uidb64 is not None and token is not None  # checked by URLconf
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = PasswordResetConfirmForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('password_reset_complete')
        else:
            form = PasswordResetConfirmForm(user)
        return render(request, 'user_onboarding/password_reset_confirm.html', {'form': form})
    else:
        return HttpResponse('The reset password link is no longer valid!')
