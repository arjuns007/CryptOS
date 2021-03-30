from django.apps import AppConfig


class PositionsConfig(AppConfig):
    name = 'positions'

    def ready(self):
        import positions.signals

