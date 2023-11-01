
# Register your models here.
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import FileData, FolderData


class StorageDetails(admin.ModelAdmin):
    list_display = ('pk_name_location', 'name', 'location', 'timestamp')

class FodlerDetails(admin.ModelAdmin):
    list_display = ('pk', 'name', 'location', 'timestamp', 'num_files', 'display_files')

    def display_files(self, obj):
        return ', '.join([str(file) for file in obj.files.all()])
    display_files.short_description = 'Files'

admin.site.register(FileData, StorageDetails)
admin.site.register(FolderData, FodlerDetails)
