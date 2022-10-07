from decimal import Decimal
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import session
from werkzeug.datastructures import MultiDict
from src.services.discipline import DisciplineService
from src.web.forms.discipline.forms import CreateDisciplineForm
from src.errors import database
from src.web.helpers.auth import login_required, verify_permission

# Se define Blueprint de Usuario
discipline_blueprint = Blueprint("discipline", __name__, url_prefix="/disciplinas")
service = DisciplineService()


@discipline_blueprint.get("/")
@login_required
def index():
    """Render de la lista de disciplinas con paginación"""

    page = request.args.get("page", 1, type=int)
    
    disciplines = service.list_disciplines(page)
    
    next_url = (
        url_for("discipline.index", page=disciplines.next_num)
        if disciplines.has_next
        else None
    )
    prev_url = (
        url_for("discipline.index", page=disciplines.prev_num)
        if disciplines.has_prev
        else None
    )
    return render_template(
        "disciplines/index.html",
        disciplines=disciplines.items,
        next_url=next_url,
        prev_url=prev_url,
    )


@discipline_blueprint.get("/add")
@login_required
@verify_permission("discipline_new")
def add_form():
    form_data = session.get("formdata", None)
    if form_data:
        form = CreateDisciplineForm(MultiDict(form_data))
        session.pop("formdata")
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
        flash("Disciplina creada con éxito", "success")
    except database.AmountValueError as e:
        flash(e, "error")
        session["formdata"] = request.form
        return redirect(request.referrer)
    except database.ExistingData as e:
        flash(e, "error")
        session["formdata"] = request.form
        return redirect(request.referrer)

    return redirect(url_for("discipline.index"))
