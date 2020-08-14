from django.apps import AppConfig


class CamroidAppConfig(AppConfig):
    name = 'camroid_app'

    def ready(self):
        import camroid_app.signals