from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, EmailField, PasswordField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email


class UserBaseForm(FlaskForm):
    email = EmailField(
        "Email", validators=[DataRequired(), Length(max=50, min=3), Email()]
    )
    username = StringField(
        "Usuario", validators=[DataRequired(), Length(max=30, min=3)]
    )
    first_name = StringField(
        "Nombre", validators=[DataRequired(), Length(max=75, min=3)]
    )
    last_name = StringField(
        "Apellido", validators=[DataRequired(), Length(max=75, min=3)]
    )


class CreateUserForm(UserBaseForm):
    roles = SelectField(
        "Rol",
        choices=[
            ("Administrador", "Administrador"),
            ("Operador", "Operador"),
            ("Socio", "Socio"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Crear usuario")


class UpdateUserForm(UserBaseForm):
    submit = SubmitField("Actualizar usuario")


class SearchUserForm(FlaskForm):
    email = EmailField(
        "Email", validators=[DataRequired(), Length(max=50, min=3), Email()]
    )
    submit = SubmitField("Buscar usuario")


class FilterUsersForm(FlaskForm):
    filter = SelectField(
        "filter",
        choices=[
            ("Activo", "Activo"),
            ("Bloqueado", "Bloqueado"),
            ("Mostrar Todos", "Mostrar Todos"),
        ],
    )
    submit = SubmitField("Filtrar")


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


class LoginForm(FlaskForm):
    username = StringField(
        "username", validators=[DataRequired(), Length(max=30, min=3)]
    )
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("Login")

class UnlinkMemberForm(FlaskForm):
    member = StringField("member", validators=[DataRequired()])
    submit = SubmitField("Desvincular Socio")

class UpdatePassForm(FlaskForm):
    current_password = PasswordField("Contraseña Actual", validators=[DataRequired()])
    new_password = PasswordField("Contraseña Nueva", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirmar contraseña", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Cambiar")