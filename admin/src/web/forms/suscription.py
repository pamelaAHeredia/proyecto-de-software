from flask_wtf import FlaskForm
from wtforms import EmailField, SubmitField
from wtforms.validators import InputRequired, Email


class SuscriptionBaseForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired(),Email()])

class SuscriptionSearchForm(SuscriptionBaseForm):
    submit = SubmitField('Buscar')

class SuscriptionAddForm(SuscriptionBaseForm):
    submit = SubmitField('Inscribir')