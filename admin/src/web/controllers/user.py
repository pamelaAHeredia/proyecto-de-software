from flask import Blueprint, request, render_template, flash, redirect, url_for
from src.models import auth
from src.services.utils import hash_pass
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
    mail = request.form.get("email")
    userName = request.form.get("username")
    if (auth.mail_not_exists(mail)):
        if(auth.username_not_exists(userName)):
            data_user = {
                "email": mail,
                "username": userName,
                "password": hash_pass(request.form.get("email")),
                "first_name": request.form.get("first_name"),
                "last_name": request.form.get("last_name"),
            }
            auth.create_user(**data_user)
            flash("Usuario creado con éxito!", "success")
        else: 
            flash("El nombre de usuario ya se encuentra registrado.", "danger") 
    else: 
        flash("El mail ingresado ya se encuentra registrado.", "danger")

    return redirect(url_for("users.users_index"))  

#Eliminar un usuario
@user_blueprint.route("/delete/<id>")
def users_delete(id):
    auth.delete_user(id)
    flash("Usuario eliminado exitosamente.", "success")
    return redirect(url_for("users.users_index")) 


#actualización de datos de un usuario
@user_blueprint.route("/update/<id>", methods = ['POST', 'GET'])
def users_update(id):
    user = auth.find_user(id)
    if request.method == "POST":
        mail = request.form.get("email")
        userName = request.form.get("username")
        
        if (auth.find_user_byEmail(mail).id == int(id)):
            if(auth.find_user_byUsername(userName).id == int(id)):
                data_user = {
                    "email": mail,
                    "username": userName,
                    "first_name": request.form.get("first_name"),
                    "last_name": request.form.get("last_name"),
                }
                
                auth.update_user(id, **data_user)
                flash("Usuario actualizado con éxito!", "success")
                return render_template("users/update.html", user=user)
            else: 
                flash("El nombre de usuario ya se encuentra registrado.", "danger")
                return render_template("users/update.html", user=user) 
        else: 
            flash("El mail ingresado ya se encuentra registrado.", "danger")
            return render_template("users/update.html", user=user) 
    else:
        return render_template("users/update.html", user=user)

#Buscar un usuario

@user_blueprint.route("/search", methods = ['GET'])
def users_search():
    input = request.form.get("value")

    if(input == "activo"):
        return "búsqueda activo/inactivo"
    else:
        return "busqueda por mail?"