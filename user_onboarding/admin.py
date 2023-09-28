from django.contrib import admin
from .models import PhoneNumber, Request_User


class PhoneNumberInline(admin.StackedInline):
    model = PhoneNumber
    can_delete = False
    verbose_name_plural = 'Phone Number'


class RequestUserAdmin(admin.ModelAdmin):
    exclude = ('user_password',)
    inlines = [PhoneNumberInline]


admin.site.register(Request_User, RequestUserAdmin)
admin.site.register(PhoneNumber)
