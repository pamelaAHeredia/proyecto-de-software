from src.models.database import db
from src.models.settings import Settings
from copy import copy

class SettingsService:
    """Esta clase maneja el servicio de configuraciones"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SettingsService, cls).__new__(cls)
        return cls._instance

    def load_settings(self,
                    itemsPerPage,
                    enablePaytable,
                    contactInfo,
                    textHeaderPayment,
                    amountMonthly,
                    percentageSurcharge):
        """Metodo que carga las configuraciones"""
        if (Settings.query.get(1) is None):
            settings = Settings(
                                itemsPerPage,
                                enablePaytable,
                                contactInfo,
                                textHeaderPayment,
                                amountMonthly,
                                percentageSurcharge)
            db.session.add(settings)
        else:
            settings = Settings.query.get(1)
            settings.items_per_page = itemsPerPage
            settings.enable_paytable = enablePaytable
            settings.contact_info = contactInfo
            settings.text_header_payment = textHeaderPayment
            settings.amount_monthly = amountMonthly
            settings.percentage_surcharge = percentageSurcharge
        db.session.commit()

    def get_settings(self):
        return Settings.query.get(1)
    