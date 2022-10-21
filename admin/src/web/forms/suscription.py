from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField, IntegerField, BooleanField
from wtforms.validators import InputRequired, NumberRange, Length, Optional


class SuscriptionForm(FlaskForm):
    pass