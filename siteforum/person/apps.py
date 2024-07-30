from django.apps import AppConfig


class PersonConfig(AppConfig):
    verbose_name = 'Персоны'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'person'
