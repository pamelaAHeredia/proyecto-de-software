from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField, IntegerField, BooleanField
from wtforms.validators import InputRequired, NumberRange, Length, Optional


class DisciplineBaseForm(FlaskForm):
    name = StringField("Disciplina", validators=[InputRequired()])
    category = StringField("Categoria", validators=[InputRequired()])
    instructor = StringField("Instructor/es", validators=[InputRequired()])
    days_and_schedules = StringField("Día y Horario", validators=[InputRequired()])
    registration_quota = IntegerField(
        "Cupos", validators=[InputRequired(), NumberRange(min=1)]
    )
    pays_per_year = IntegerField(
        "Pagos por año", validators=[InputRequired(), NumberRange(min=1)]
    )
    amount = DecimalField("Precio", validators=[InputRequired(), NumberRange(min=0)])
    is_active = BooleanField("¿Activa?", default=True, validators=[Optional()])


class CreateDisciplineForm(DisciplineBaseForm):
    submit = SubmitField("Guardar")


class UpdateDisciplineForm(CreateDisciplineForm):
    submit = SubmitField("Actualizar")
