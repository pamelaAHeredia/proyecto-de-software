from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import InputRequired, Email


class SuscriptionForm(FlaskForm):
    document_type = SelectField("Tipo de Documento", choices=["DNI","LE","LC","PASAPORTE"])
    document_number = StringField("Número de Documento", validators=[InputRequired()])
    submit = SubmitField('Buscar')
