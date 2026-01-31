from django.apps import AppConfig


class HmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hms'

    def ready(self):
        # Import your signals when the app is ready
        try:
            import hms.signals
        except ImportError:
            pass
