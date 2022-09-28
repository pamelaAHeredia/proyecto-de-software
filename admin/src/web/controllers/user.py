from flask import Blueprint, request, render_template
from src.models.auth.user import User
from src.models import auth

user_blueprint = Blueprint("users", __name__, url_prefix="/users")


@user_blueprint.route("/")
def users_index():
    users = auth.list_users()

    return render_template("users/index.html", users=users)


"""
@user_blueprint.route("/issues/add", methods=["POST"])
def issues_add():
    issue = {
        "id": request.form.get("id"),
        "user": request.form.get("user"),
        "title": request.form.get("title"),
        "description": request.form.get("description"),
        "status": request.form.get("status"),
    }
    issues.append(issue)
    return render_template("issues/index.html", issues=issues) """
