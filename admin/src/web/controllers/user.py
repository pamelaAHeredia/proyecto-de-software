from flask import Blueprint, request, render_template
from src.models.auth.user import User
from src.models import auth
from src.models.auth.utils import hash_pass


user_blueprint = Blueprint("users", __name__, url_prefix="/users")


@user_blueprint.route("/")
def users_index():
    users = auth.list_users()

    return render_template("users/index.html", users=users)


@user_blueprint.route("/add", methods=["POST"])
def users_add():
    data_user = {
        "email": request.form.get("email"),
        "username": request.form.get("username"),
        "password": hash_pass(request.form.get("email")),
        "first_name": request.form.get("first_name"),
        "last_name": request.form.get("last_name"),
    }
    auth.create_user(**data_user)
    return users_index()
