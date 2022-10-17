from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, Length

class SettingsForm(FlaskForm):
    """Clase de formulario de settings"""
    items_per_page = IntegerField("Items por pagina", validators=[
                                                            DataRequired(), 
                                                            NumberRange(min=1)])
    enable_paytable = BooleanField("Habilitar tabla de pagos")
    contact_info = TextAreaField("Informacion de contacto", validators=[
                                                            DataRequired(),
                                                            Length(min=5,max=100)])
    text_header_payment = StringField("Texto encabezado de pago",validators=[
                                                            DataRequired(),
                                                            Length(min=3,max=30)])
    amount_monthly = DecimalField("Precio mensual",validators=[
                                                            DataRequired(),
                                                            NumberRange(min=0)])
    percentage_surcharge = DecimalField("Porcentaje de recarga", validators=[
                                                            DataRequired(),
                                                            NumberRange(min=0)])