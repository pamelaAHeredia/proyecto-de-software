from src.models.database import db


class Settings(db.Model):
    """Clase del modelo de configuraciones del sistema"""
    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    items_per_page = db.Column(db.Integer, default=2)
    enable_paytable = db.Column(db.Boolean, default=True)
    contact_info = db.Column(db.String(150), nullable = False)
    text_header_payment = db.Column(db.String(50), nullable = False)
    amount_monthly = db.Column(db.Integer, default=100)
    percentage_surcharge = db.Column(db.Integer, default=0)

    def __init__(self, 
                items_per_page, 
                enable_paytable, 
                contact_info, 
                text_header_payment, 
                amount_monthly, 
                percentage_surcharge):  
        self.items_per_page = items_per_page
        self.enable_paytable = enable_paytable
        self.contact_info = contact_info
        self.text_header_payment = text_header_payment
        self.amount_monthly = amount_monthly
        self.percentage_surcharge = percentage_surcharge