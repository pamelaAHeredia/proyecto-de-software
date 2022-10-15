from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length


class CreateUserForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Length(max=50, min=3)])
    username = StringField(
        "Usuario", validators=[DataRequired(), Length(max=30, min=3)]
    )
    first_name = StringField(
        "Nombre", validators=[DataRequired(), Length(max=75, min=3)]
    )
    last_name = StringField(
        "Apellido", validators=[DataRequired(), Length(max=75, min=3)]
    )
    roles = SelectField(
        "Rol",
        choices=[("Administrador", "Administrador"), ("Operador", "Operador")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Crear usuario")


class UpdateUserForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Length(max=50, min=3)])
    username = StringField(
        "Usuario", validators=[DataRequired(), Length(max=30, min=3)]
    )
    first_name = StringField(
        "Nombre", validators=[DataRequired(), Length(max=75, min=3)]
    )
    last_name = StringField(
        "Apellido", validators=[DataRequired(), Length(max=75, min=3)]
    )
    submit = SubmitField("Actualizar usuario")


class SearchUserForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Length(max=50, min=3)])
    submit = SubmitField("Buscar usuario")


class FilterUsersForm(FlaskForm):
    filter = SelectField(
        "filter",
        choices=[
            ("activo", "activo"),
            ("bloqueado", "bloqueado"),
            ("ninguno", "ninguno"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Filtar")


class AddRolesForm(FlaskForm):
    roles = SelectField(
        "Rol",
        choices=[
            ("Administrador", "Administrador"),
            ("Operador", "Operador"),
            ("Socio", "socio"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Crear usuario")

class DeleteRolesForm(FlaskForm):
    role = StringField("role", validators=[DataRequired()])
    submit = SubmitField("Eliminar rol")