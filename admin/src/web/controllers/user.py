from flask import Blueprint, request, render_template, flash
from src.models.auth.user import User
from src.models import auth
from src.models.auth.utils import hash_pass

# Se define Blueprint de Usuario
user_blueprint = Blueprint("users", __name__, url_prefix="/users")


@user_blueprint.get("/")
def users_index():
    """Por metodo GET pide la lista total de usuarios al modelo y lo renderiza en la vista"""
    users = auth.list_users()

    return render_template("users/index.html", users=users)


@user_blueprint.post("/add")
def users_add():
    """Por metodo POST toma del request los datos y se los pasa al modelo para que agregue un Usuario"""
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

