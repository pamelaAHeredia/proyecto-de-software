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
        """Metodo que obtiene todas las configuraciones"""
        return Settings.query.get(1)
    
    def get_items_per_page(self):
        """Metodo que obtiene los elementos por pagina"""
        return Settings.query.get(1).items_per_page

    def get_enable_paytable(self):
        """Metodo que obtiene si esta habilitado la tabla de pagos"""
        return Settings.query.get(1).enable_paytable

    def get_contact_info(self):
        """Metodo que obtiene la informacion de contacto"""
        return Settings.query.get(1).contact_info

    def get_text_header_payment(self):
        """Metodo que obtiene el texto de encabezado en el recibo de pago"""
        return Settings.query.get(1).text_header_payment

    def get_amount_monthly(self):
        """Metodo que obtiene el monto base mensual"""
        return Settings.query.get(1).amount_monthly

    def get_percentage_surcharge(self):
        """Metodo que obtiene el porcentaje de recarga"""
        return Settings.query.get(1).percentage_surcharge