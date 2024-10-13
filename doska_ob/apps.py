from django.apps import AppConfig


class Doska_obConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "doska_ob"

    def ready(self):
        import doska_ob.signals