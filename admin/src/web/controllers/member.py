from flask import Blueprint, request, render_template, flash, redirect, url_for

from src.services.member import MemberService
from src.errors import database 


# Se define Blueprint de Socio
member_blueprint = Blueprint("members", __name__, url_prefix="/socios")


service = MemberService()

@member_blueprint.get("/")
def members_index():
    """Por metodo GET pide la lista total de socios al modelo y lo renderiza en la vista"""
    members = service.list_members()
    return render_template("members/index.html", members=members)


@member_blueprint.post("/add")
def members_add():
    """Por metodo POST toma del request los datos y se los pasa al modelo para que agregue un Socio,
       si no lo puede agregar lo informa"""
    data_member = {
        "first_name": request.form.get("first_name"),
        "last_name": request.form.get("last_name"),
        "document_type": request.form.get("document_type"),  
        "document_number": request.form.get("document_number"), 
        "gender": request.form.get("gender"), 
        "address": request.form.get("address"),  
        "email": request.form.get("email"),
        "phone_number": request.form.get("phone_number"),
    }
    try:
        service.create_member(**data_member)
        flash("Socio guardado con éxito!", "success")
    except database.ExistingData as e:
        flash(e,"danger")
    return redirect(url_for("members.members_index"))



