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
    discipline_paginator = service.list_paginated_disciplines(
        page, 2, "discipline.index"
    )

    return render_template(
        "disciplines/index.html",
        disciplines=discipline_paginator.items,
        next_url=discipline_paginator.next_url,
        prev_url=discipline_paginator.prev_url,
    )


@discipline_blueprint.route("/create", methods=["GET", "POST"])
@login_required
@verify_permission("discipline_create")
def create():
    form = CreateDisciplineForm()

    if form.validate_on_submit():

        name = form.name.data
        category = form.category.data
        instructor_first_name = form.instructor_first_name.data
        instructor_last_name = form.instructor_last_name.data
        days_and_schedules = form.days_and_schedules.data
        registration_quota = form.registration_quota.data
        amount = form.amount.data

        try:
            service.create_discipline(
                name=name,
                category=category,
                instructor_first_name=instructor_first_name,
                instructor_last_name=instructor_last_name,
                days_and_schedules=days_and_schedules,
                registration_quota=registration_quota,
                amount=amount,
            )
            flash("Disciplina creada con éxito", "success")
            return redirect(url_for("discipline.index"))
        except database.MinValueValueError as e:
            flash(str(e), "danger")
        except database.ExistingData as e:
            flash(f"La disciplina: {name} - {category} ya existe.", "danger")
    return render_template("disciplines/create.html", form=form)
