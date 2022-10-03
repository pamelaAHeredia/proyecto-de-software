from flask import Blueprint, request, render_template, flash
from src.models.club.discipline import Discipline
from src.models.club import list_disciplines, create_discipline

# Se define Blueprint de Usuario
discipline_blueprint = Blueprint("discipline", __name__, url_prefix="/disciplinas")


@discipline_blueprint.get("/")
def discipline_index():
    """Render de la lista de usuarios"""
    disciplines = list_disciplines()

    return render_template("disciplines/index.html", disciplines=disciplines)


@discipline_blueprint.post("/add")
def discipline_add():
    data_discipline = {
        "name": request.form.get("name"),
        "category": request.form.get("category"),
        "instructor_first_name": request.form.get("instructor_first_name"),
        "instructor_last_name": request.form.get("instructor_last_name"),
        "days_and_schedules": request.form.get("days_and_schedules"),
        "amount": request.form.get("amount"),
    }
    
    if int(data_discipline["amount"]) <= 0:
        flash("Se debe agregar un monto mayor a 0", "error")
        return discipline_index()
    
    discipline = Discipline.find_discipline(
        data_discipline["name"], data_discipline["category"]
    )

    if not discipline:
        create_discipline(**data_discipline)
        flash("Disciplina guardada con éxito!", "success")
        return discipline_index(), 200

    flash("Ya existe la disciplina", "error")
    return discipline_index()
