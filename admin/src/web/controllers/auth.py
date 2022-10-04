from flask import Blueprint
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import session
from src.services.login import find_user_by_mail_and_pass

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@auth_blueprint.get("/")
def login ():
    """Render del login del sistema"""
    return render_template("auth/login.html")

@auth_blueprint.post("/authenticate")
def authenticate():
    """Verifica si los datos son correctos y logea o vuelve a pantalla login"""
    params = request.form
    user = find_user_by_mail_and_pass(params["email"], params["password"])
    if not user:
        flash("Email o clave incorrecta", "error")
        return redirect(url_for("auth.login"))
    session["user"] = user.email
    flash("La sesión se inicio correctamente.", "success")

    return redirect(url_for("home"))

@auth_blueprint.get("/logout")
def logout():
    """Cerrar sesion del sistema"""
    del session["user"]
    session.clear()
    flash("La sesion se cerro correctamente.", "success")

    return redirect(url_for("auth.login"))
