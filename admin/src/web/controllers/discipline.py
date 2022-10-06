from decimal import Decimal
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import session
from werkzeug.datastructures import MultiDict
from src.services.discipline import DisciplineService
from src.web.forms.discipline.forms import CreateDisciplineForm
from src.errors import database
from src.web.helpers.auth import login_required

# Se define Blueprint de Usuario
discipline_blueprint = Blueprint("discipline", __name__, url_prefix="/disciplinas")
service = DisciplineService()


@discipline_blueprint.get("/")
@login_required
def index():
    """Render de la lista de disciplinas"""
    disciplines = service.list_disciplines()

    return render_template("disciplines/index.html", disciplines=disciplines)


@discipline_blueprint.get("/add")
@login_required
def add_form():
    form_data = session.get('formdata', None)
    if form_data:
        form = CreateDisciplineForm(MultiDict(form_data))
        session.pop('formdata')
    else:
        form = CreateDisciplineForm()
    return render_template("disciplines/create.html", form=form)


@discipline_blueprint.post("/create")
@login_required
def create():
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
        session['formdata'] = request.form
        return redirect(request.referrer)
    except database.ExistingData as e:
        flash(e, "error")
        session['formdata'] = request.form
        return redirect(request.referrer)

    return redirect(url_for("discipline.index"))
