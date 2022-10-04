from flask import Blueprint, request, render_template, flash
from src.models.auth.user import User
from src.models import auth
from src.models.auth.utils import hash_pass
from src.web.helpers.auth import login_required

# Se define Blueprint de Usuario
user_blueprint = Blueprint("users", __name__, url_prefix="/users")


@user_blueprint.get("/")
@login_required
def users_index():
    """Render de la lista de usuarios """
    users = auth.list_users()

    return render_template("users/index.html", users=users)


@user_blueprint.post("/add")
@login_required
def users_add():
    """Agrega usuarios mediante el formulario"""
    data_user = {
        "email": request.form.get("email"),
        "username": request.form.get("username"),
        "password": hash_pass(request.form.get("email")),
        "first_name": request.form.get("first_name"),
        "last_name": request.form.get("last_name"),
    }
    auth.create_user(**data_user)
    flash("Usuario guardado con éxito!")
    return users_index() 

