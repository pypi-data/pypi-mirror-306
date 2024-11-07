from django.apps import AppConfig
from django.conf import settings


class DjangoldpEnergiepartageeConfig(AppConfig):
    name = "djangoldp_energiepartagee"
    if getattr(settings, "IS_AMORCE", False):
        verbose_name = "AMORCE"
    else:
        verbose_name = "Énergie Partagée"

    def ready(self):
        from djangoldp_energiepartagee.models.discount import Discount
        from djangoldp_energiepartagee.models.payment_method import \
            Paymentmethod

        Discount.objects.get_or_create(name="villageoise")
        Paymentmethod.objects.get_or_create(name="Virement")
