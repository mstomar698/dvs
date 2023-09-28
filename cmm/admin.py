from django.contrib import admin
from .models import Cmm_Sick,CsvFile,Cmm_pro,Cmm_Warranty,Cmm_Warranty_New,Failed_Assembly


class MISADMIN(admin.ModelAdmin):
    search_fields = ['__all__']

admin.site.register(Cmm_Sick,MISADMIN)
admin.site.register(CsvFile)
admin.site.register(Cmm_pro)
admin.site.register(Cmm_Warranty)
admin.site.register(Cmm_Warranty_New)
admin.site.register(Failed_Assembly)
