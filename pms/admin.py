from django.contrib import admin

from .models import Device, Sensor, Data

# Register your models here.

admin.site.register(Device)
admin.site.register(Sensor)

# admin.site.register(Data)


class PMSAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)
    search_fields = ['sensor__name', 'device__uname', 'data', 'created_at']


admin.site.register(Data, PMSAdmin)
