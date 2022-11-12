from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import DataRequired, NumberRange

class PaymentForm(FlaskForm):
    """Clase de formulario de añadir cuota mensual"""
    month = IntegerField("Mes", validators=[
                                                            DataRequired(), 
                                                            NumberRange(min=1,max=12)])
    year = IntegerField("Año", validators=[
                                                            DataRequired(), 
                                                            NumberRange(min=2000,max=2100)])