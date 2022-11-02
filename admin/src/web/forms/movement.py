from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, DateField, SubmitField 
from wtforms.validators import InputRequired, NumberRange, DataRequired, Length

class MovementBaseForm(FlaskForm):
    amount =  DecimalField("Monto", validators=[InputRequired(), NumberRange(min=0)])
    detail = StringField("Descripción", validators=[DataRequired(), Length(min=3, max=70)])
    date = DateField("Fecha", format='%m/%d/%y')

class CreateMovementForm(MovementBaseForm): 
    submit = SubmitField("Registrar pago")