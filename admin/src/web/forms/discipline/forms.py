from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField


class CreateDisciplineForm(FlaskForm):
    name = StringField("name")
    category = StringField("category")
    instructor_first_name = StringField("instructor_first_name")
    instructor_last_name = StringField("instructor_last_name")
    days_and_schedules = StringField("days_and_schedules")
    amount = DecimalField("amount")