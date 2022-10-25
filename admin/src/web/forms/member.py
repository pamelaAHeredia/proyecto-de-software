from flask import flash
from flask_wtf import FlaskForm
from traitlets import default
from wtforms import StringField, SubmitField, SelectField, EmailField
from wtforms.validators import (
    InputRequired,
    Email,
    Optional,
    DataRequired,
    Length,
    ValidationError,
)


class MemberForm(FlaskForm):
    first_name = StringField("Nombre", validators=[InputRequired()])
    last_name = StringField("Apellido", validators=[InputRequired()])
    document_type = SelectField(
        "Tipo de Documento", choices=["DNI", "LE", "LC", "PASAPORTE"]
    )
    document_number = StringField(
        "Número de Documento", validators=[InputRequired(), Length(min=8, max=10)]
    )

    def validate_document_number(form, field):
        if not field.data.isdigit():
            flash("Solo caracteres numéricos para el N° de Documento", "danger")
            raise ValidationError()

    gender = SelectField("Género", choices=["M", "F", "Otro"])
    address = StringField("Domicilio", validators=[InputRequired()])
    email = EmailField("Email", validators=[Optional(), Email()])
    phone_number = StringField("Teléfono")
    submit = SubmitField("Guardar")


class FilterSearchForm(FlaskForm):
    filter = SelectField(
        "Filtro",
        choices=[
            ("Todos", "Todos"),
            ("Activos", "Activos"), 
            ("Inactivos", "Inactivos"),
        ], default=("Todos")
    )
    search = StringField("Apellido")
    submit = SubmitField("Filtrar")


class FilterByDocForm(FlaskForm):
    document_number = StringField(
        "Número de Documento", validators=[DataRequired(), Length(min=8, max=10)]
    )
    document_type = SelectField(
        "Tipo de Documento", choices=["DNI", "LE", "LC", "PASAPORTE"]
    )
    submit = SubmitField("Buscar Socio")

    

