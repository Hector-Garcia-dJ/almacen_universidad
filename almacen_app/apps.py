from django.apps import AppConfig


class AlmacenAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'almacen_app'

INSTALLED_APPS = (
    # ...
    'qr_code',
)
