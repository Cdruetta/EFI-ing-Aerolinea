from django.apps import AppConfig


class GestionvuelosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gestionVuelos"


    def ready(self):
        import gestionVuelos.signals
