from decimal import Decimal
from flask import Blueprint, request, render_template, flash
from src.services.discipline import DisciplineService
from src.web.forms.discipline.forms import CreateDisciplineForm
from src.errors import database
from src.web.helpers.auth import login_required

# Se define Blueprint de Usuario
discipline_blueprint = Blueprint("discipline", __name__, url_prefix="/disciplinas")
service = DisciplineService()


@discipline_blueprint.get("/")
@login_required
def discipline_index():
    """Render de la lista de usuarios"""
    form = CreateDisciplineForm()
    disciplines = service.list_disciplines()

    return render_template("disciplines/index.html", disciplines=disciplines, form=form)


@discipline_blueprint.post("/add")
@login_required
def discipline_add():

    name = request.form.get("name")
    category = request.form.get("category")
    instructor_first_name = request.form.get("instructor_first_name")
    instructor_last_name = request.form.get("instructor_last_name")
    days_and_schedules = request.form.get("days_and_schedules")
    amount = request.form.get("amount")

    try:
        service.create_discipline(
            name=name,
            category=category,
            instructor_first_name=instructor_first_name,
            instructor_last_name=instructor_last_name,
            days_and_schedules=days_and_schedules,
            amount=amount,
        )
    except database.AmountValueError as e:
        flash(e, "error")
        return discipline_index()
    except database.ExistingData as e:
        flash(e, "error")
        return discipline_index()
