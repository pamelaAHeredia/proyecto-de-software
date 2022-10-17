from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, EmailField
from wtforms.validators import InputRequired, Email, Optional


class MemberForm(FlaskForm):
    first_name = StringField("Nombre", validators=[InputRequired()])
    last_name = StringField("Apellido", validators=[InputRequired()])
    document_type = SelectField("Tipo de Documento", choices=["DNI","LE","LC","PASAPORTE"])
    document_number = StringField("Número de Documento", validators=[InputRequired()])
    gender = SelectField("Género", choices=["M","F","Otro"])
    address = StringField("Domicilio", validators=[InputRequired()])
    email = EmailField("Email", validators=[Optional(),Email()])
    phone_number = StringField("Teléfono")
    submit = SubmitField('Guardar')