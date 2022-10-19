from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField
from wtforms.validators import DataRequired, NumberRange, Length

class CreateDisciplineForm(FlaskForm):
    name = StringField("Disciplina", validators=[DataRequired()])
    category = StringField("Categoria", validators=[DataRequired()])
    instructor_first_name = StringField("Nombre del Instructor", validators=[DataRequired()])
    instructor_last_name = StringField("Apellido del Instructor", validators=[DataRequired()])
    days_and_schedules = StringField("Día y Horario", validators=[DataRequired()])
    amount = DecimalField("Precio", validators=[DataRequired(), NumberRange(min=0)])

