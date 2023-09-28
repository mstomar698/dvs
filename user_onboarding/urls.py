from django.urls import path
from django.shortcuts import redirect, render

from user_onboarding.src import email_otp

from .src import login_register, edit_profile, requested_user, forget_password, otp_auth
from django.contrib.auth.views import LogoutView
import django.contrib.auth.views as auth_views


urlpatterns = [
    #     create a path to redirect to login on /
    path("", lambda request : redirect('login/') , name="redirect_login"),

    path("login/", login_register.user_login, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # path("register_user/", login_register.register_user, name="register_user"),
    path(
        "change_password/change/", edit_profile.change_password, name="change_password"
    ),

    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="user_onboarding/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        forget_password.PasswordResetConfirmView,
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="user_onboarding/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path(
        "forget_password/",
        forget_password.password_reset_request,
        name="password_reset",
    ),

    path("request_user/", requested_user.request_user, name="request_user"),
    path(
        "show_user_requested/",
        requested_user.show_requested_user,
        name="show_requested_user",
    ),
    path(
        "user_requested/<int:user_id>/<str:arg>/",
        requested_user.requested_user,
        name="requested_user",
    ),
    path("user_profile/", edit_profile.user_profile, name="user_profile"),
    path('selector/', login_register.selector , name='selector'),

    path('otp_auth/', otp_auth.otp_auth , name='otp_auth'),
    path('otp_val/', otp_auth.otp_val , name='otp_val'),
    path('otp_confirm/', otp_auth.otp_confirm , name='otp_confirm'),
    path('email_otp_send/', email_otp.email_otp_send , name='email_otp_send'),
    path('email_otp_val/', email_otp.email_otp_val , name='email_otp_val'),
    path('phone_otp_send/', otp_auth.phone_otp_send , name='phone_otp_send'),
    path('phone_otp_val/', otp_auth.phone_otp_val , name='phone_otp_val'),

]
