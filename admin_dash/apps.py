from django.apps import AppConfig


class AdminDashConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_dash'


class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        from jobs import updater
        
        updater.start()