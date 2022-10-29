from django.apps import AppConfig


class TorismappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'torismApp'

    def ready(self): # registering our signal with the app
        import torismApp.signals
