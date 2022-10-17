from flask import Blueprint
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import session
from src.services.user import UserService
from src.errors import database
from src.web.forms.user import LoginForm

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")
service = UserService()


@auth_blueprint.get("/")
def login():
    login_form = LoginForm()
    """Render del login del sistema"""
    return render_template("auth/login.html", login_form=login_form)


@auth_blueprint.post("/authenticate")
def authenticate():
    """Verifica si los datos son correctos y logea o vuelve a pantalla login"""
    login_form = LoginForm()
    if login_form.validate_on_submit:
        try:
            email = login_form.email.data
            password = login_form.password.data
            user = service.find_user_by_mail_and_pass(email, password)
            session["user"] = user.email
            flash("La sesión se inicio correctamente.", "success")
        except database.PermissionDenied as e:
            flash(e, "danger")
            return redirect(url_for("auth.login"))

    return redirect(url_for("home"))


@auth_blueprint.get("/logout")
def logout():
    """Cerrar sesion del sistema"""
    del session["user"]
    session.clear()
    flash("La sesion se cerro correctamente.", "success")

    return redirect(url_for("auth.login"))
