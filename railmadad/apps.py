from django.apps import AppConfig
from railmadad.constants import update_global_variables


class RailmadadConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'railmadad'
    def ready(self):
        update_global_variables()