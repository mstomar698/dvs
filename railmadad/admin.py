from django.contrib import admin 
from .models import Main_Data_Upload,CsvFile,Train_Type,MIS_DATA,Staff_Detail


# Register your models here.
class MISADMIN(admin.ModelAdmin):
    search_fields = ['reference_number','registration_date','staff_name','physical_coach_number','train_station','problem_type','sub_type']

admin.site.register(Main_Data_Upload,MISADMIN)
admin.site.register(CsvFile)
admin.site.register(Train_Type)
admin.site.register(MIS_DATA)
admin.site.register(Staff_Detail)