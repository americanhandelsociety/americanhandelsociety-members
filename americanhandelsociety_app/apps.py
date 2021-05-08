from django.apps import AppConfig


class AmericanHandelSocietyAppConfig(AppConfig):
    name = "americanhandelsociety_app"

    def ready(self):
        from paypal.standard.ipn.signals import valid_ipn_received
        from .signals import listen_for_paypal_please

        valid_ipn_received.connect(listen_for_paypal_please)
