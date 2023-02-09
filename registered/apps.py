from django.apps import AppConfig


class RegisteredConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'registered'
    verbose_name = "Records"
