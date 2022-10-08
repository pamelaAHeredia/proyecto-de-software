from flask import Blueprint, request, render_template, flash
from src.models.auth.user import User
from src.models import auth
from src.services.utils import hash_pass
from src.web.helpers.auth import login_required
from flask import Blueprint, request, render_template, flash, redirect, url_for
from src.services.user import UserService
from src.models.auth.utils import hash_pass


user_blueprint = Blueprint("users", __name__, url_prefix="/users")

service = UserService()


@user_blueprint.get("/")
@login_required
def users_index():
    """Por metodo GET pide la lista total de usuarios al modelo y lo renderiza en la vista"""
    users = service.list_users()
    return render_template("users/index.html", users=users)


<<<<<<< admin/src/web/controllers/user.py
@user_blueprint.post("/add")
@login_required
def users_add():
    """Agrega usuarios mediante el formulario"""
=======
@user_blueprint.route("/add", methods=["POST"])
def users_add():

>>>>>>> admin/src/web/controllers/user.py
    data_user = {
        "email": request.form.get("email"),
        "username": request.form.get("username"),
        "password": hash_pass(request.form.get("email")),
        "is_active": True,
        "first_name": request.form.get("first_name"),
        "last_name": request.form.get("last_name"),
        "blocked": False,
    }
    added_user = service.create_user(**data_user)
    if added_user:
        flash("Usuario creado con éxito!", "success")
    else:
        flash("El coso ya está guardado", "danger")
    return redirect(url_for("users.users_index"))


@user_blueprint.route("/update/<id>", methods=["POST", "GET"])
def users_update(id):
    user = service.find_user_by_id(id)
    if request.method == "POST":
        data_user = {
            "email": request.form.get("email"),
            "username": request.form.get("username"),
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
        }

        updated = service.update_user(id, **data_user)
        if updated:
            flash("Usuario actualizado con éxito!", "success")
        else:
            flash("El coso ya existe", "danger")
        return render_template("users/update.html", user=user)
    else:
        return render_template("users/update.html", user=user)


@user_blueprint.route("/block_user/<id>", methods=["GET"])
def users_block(id):
    service.block_user(id)
    return redirect(url_for("users.users_index"))
