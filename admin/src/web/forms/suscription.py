from flask_wtf import FlaskForm
from wtforms import EmailField, SubmitField
from wtforms.validators import InputRequired, Email


class SuscriptionForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired(),Email()])
    submit = SubmitField('Buscar')
